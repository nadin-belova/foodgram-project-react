
#from drf_extra_fields.fields import Base64ImageField
from recipes.models import Recipe
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField, CharField
)
from django.db.models import F, QuerySet


class RecipeSerializer(ModelSerializer):
    """Сериализатор для рецептов."""

    # tags = TagSerializer(many=True, read_only=True)
    # author = UserSerializer(read_only=True)
    # ingredients = SerializerMethodField()
    # is_favorited = SerializerMethodField()
    # is_in_shopping_cart = SerializerMethodField()
    # image = Base64ImageField()
    picture = CharField()

    class Meta:
        model = Recipe
        fields = '__all__'

    # def get_ingredients(self, recipe: Recipe) -> QuerySet[dict]:
    #     ingredient = recipe.ingredient.values(
    #         "id", "name", "unit", amount=F("recipe__quantity")
    #     )
    #     return ingredient
