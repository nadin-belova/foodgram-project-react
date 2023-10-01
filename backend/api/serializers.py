from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import F, QuerySet
from django.db.transaction import atomic

from drf_extra_fields.fields import Base64ImageField

from core.services import recipe_ingredients_set
from core.validators import ingredients_validator, tags_exist_validator

from recipes.models import Ingredient, Recipe, Tag
from rest_framework.serializers import ModelSerializer, SerializerMethodField


User = get_user_model()


class ShortRecipeSerializer(ModelSerializer):
    """
    Сериализатор для краткой информации о рецептах.
    """

    class Meta:
        model = Recipe
        fields = "id", "name", "image", "cooking_time"
        read_only_fields = ("__all__",)


class UserSerializer(ModelSerializer):
    """
    Сериализатор для пользователей.
    """

    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ("is_subscribed",)

    def get_is_subscribed(self, obj: User) -> bool:
        """
        Возвращает True, если текущий пользователь подписан
        на пользователя obj, иначе - False.
        """
        user = self.context.get("request").user

        if user.is_anonymous or (user == obj):
            return False

        return user.subscriptions.filter(author=obj).exists()

    def create(self, validated_data: dict) -> User:
        """
        Создает и возвращает нового пользователя.
        """
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserSubscribeSerializer(UserSerializer):
    """
    Сериализатор для подписки на пользователей.
    """

    recipes_count = SerializerMethodField(method_name='get_recipes_count')
    recipes = SerializerMethodField(method_name='get_recipes')

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )
        read_only_fields = ("__all__",)

    def get_is_subscribed(self, obj: User) -> bool:
        """
        Проверяет, подписан ли текущий пользователь на пользователя obj.
        :param obj: Пользователь, на которого проверяется подписка.
        :return: True, если текущий пользователь подписан на пользователя obj,
        иначе False.
        """
        user = self.context.get("request").user

        if user.is_anonymous or user == obj:
            return False

        return user.subscriptions.filter(author=obj).exists()

    def get_recipes_count(self, obj: User) -> int:
        """
        Возвращает количество рецептов пользователя.
        """
        return obj.recipes.count()

    def get_recipes(self, obj):
        """
        Возвращает список рецептов пользователя с ограничением по лимиту.
        """
        from api.serializers import RecipeShortSerializer
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()

        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeShortSerializer(recipes, many=True, read_only=True)
        return serializer.data


class TagSerializer(ModelSerializer):
    """
    Сериализатор для тэгов.
    """

    class Meta:
        model = Tag
        fields = "__all__"
        read_only_fields = ("__all__",)

    def validate(self, data: OrderedDict) -> OrderedDict:
        """
        Удаляет символы '#' из названия тегов и приводит к верхнему регистру.
        """
        for attr, value in data.items():
            data[attr] = value.strip(" #").upper()

        return data


class IngredientSerializer(ModelSerializer):
    """
    Сериализатор для ингредиентов.
    """

    class Meta:
        model = Ingredient
        fields = "__all__"
        read_only_fields = ("__all__",)


class RecipeSerializer(ModelSerializer):
    """
    Сериализатор для рецептов.
    """

    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = SerializerMethodField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )
        read_only_fields = (
            "is_favorite",
            "is_shopping_cart",
        )

    def get_ingredients(self, recipe: Recipe) -> QuerySet[dict]:
        """
        Возвращает информацию об ингредиентах для данного рецепта.
        """
        ingredients = recipe.ingredients.values(
            "id", "name", "measurement_unit", amount=F("recipe__amount")
        )
        return ingredients

    def get_is_favorited(self, recipe: Recipe) -> bool:
        """
        Возвращает True, если текущий пользователь
        добавил рецепт в избранное, иначе - False.
        """
        user = self.context.get("view").request.user

        if user.is_anonymous:
            return False

        return user.favorites.filter(recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe: Recipe) -> bool:
        """
        Возвращает True, если текущий пользователь
        добавил рецепт в список покупок, иначе - False.
        """
        user = self.context.get("view").request.user

        if user.is_anonymous:
            return False

        return user.carts.filter(recipe=recipe).exists()

    def validate(self, data: OrderedDict) -> OrderedDict:
        """
        Проверяет валидность данных при создании или обновлении рецепта.
        """
        tags_ids: list[int] = self.initial_data.get("tags")
        ingredients = self.initial_data.get("ingredients")

        if not tags_ids or not ingredients:
            raise ValidationError("Недостаточно данных.")

        tags = tags_exist_validator(tags_ids, Tag)
        ingredients = ingredients_validator(ingredients, Ingredient)

        data.update(
            {
                "tags": tags,
                "ingredients": ingredients,
                "author": self.context.get("request").user,
            }
        )
        return data

    @atomic
    def create(self, validated_data: dict) -> Recipe:
        """
        Создает и возвращает новый рецепт.
        """
        tags: list[int] = validated_data.pop("tags")
        ingredients: dict[int, tuple] = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        recipe_ingredients_set(recipe, ingredients)
        return recipe

    @atomic
    def update(self, recipe: Recipe, validated_data: dict):
        """
        Обновляет информацию о рецепте.
        """
        super().update(recipe, validated_data)

        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")

        if tags:
            recipe.tags.set(tags)

        if ingredients:
            recipe.ingredients.clear()
            recipe_ingredients_set(recipe, ingredients)

        recipe.save()
        return recipe
