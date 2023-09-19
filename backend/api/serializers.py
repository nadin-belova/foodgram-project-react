# from drf_extra_fields.fields import Base64ImageField
from recipes.models import Recipe, Tag, Ingredient
from users.models import MyUser
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField
)
from django.db.models import F, QuerySet


class TagSerializer(ModelSerializer):
    """Сериализатор для тэгов."""

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(ModelSerializer):
    """Сериализатор для ингридиентов."""

    class Meta:
        model = Ingredient
        fields = "__all__"


class MyUserSerializer(ModelSerializer):
    """Сериализатор для пользователей."""

    class Meta:
        model = MyUser
        fields = "__all__"


class RecipeSerializer(ModelSerializer):
    """Сериализатор для рецептов."""

    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    author = MyUserSerializer(read_only=True)
    # ingredients = SerializerMethodField()
    # is_favorited = SerializerMethodField()
    # is_in_shopping_cart = SerializerMethodField()
    # image = Base64ImageField()
    image = CharField()

    class Meta:
        model = Recipe
        fields = '__all__'

    # def get_author(self, recipe: Recipe) -> QuerySet[dict]:
    #     author = recipe.author_id.values(
    #         "id", "name", "unit", amount=F("recipe__quantity")
    #     )
    #     return author

    # def get_ingredients(self, recipe: Recipe) -> QuerySet[dict]:
    #     ingredient = recipe.ingredient.values(
    #         "id", "name", "unit", amount=F("recipe__quantity")
    #     )
    #     return ingredient
