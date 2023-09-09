from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    PROTECT,
    IntegerField,
    TextField,
)
from django.db import models


MAX_LEN_TAG_NAME_CHARFIELD = 50
MAX_LEN_TAG_COLOR_CHARFIELD = 7
MAX_LEN_TAG_SLUG_CHARFIELD = 20
MAX_LEN_INGREDIENT_CHARFIELD = 100
MAX_LEN_UNIT_CHARFIELD = 25
MAX_LEN_RECIPE_CHARFIELD = 100
MAX_LEN_PICTURE_CHARFIELD = 255


class Unit(Model):
    name = CharField(
        verbose_name="Единица измерения",
        max_length=MAX_LEN_UNIT_CHARFIELD,
    )

    class Meta:
        verbose_name = "Единица измерения"
        verbose_name_plural = "Единицы измерения"


class Tag(Model):
    name = CharField(
        verbose_name="название тэга",
        max_length=MAX_LEN_TAG_NAME_CHARFIELD
    )
    color_code = CharField(
        verbose_name="цвет тэга",
        max_length=MAX_LEN_TAG_COLOR_CHARFIELD
    )
    slug = CharField(
        verbose_name="слаг тэга",
        max_length=MAX_LEN_TAG_SLUG_CHARFIELD
    )

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"


class Ingredient(Model):
    name = CharField(
        verbose_name="Ингредиент",
        max_length=MAX_LEN_INGREDIENT_CHARFIELD,
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"


class RecipeIngredient(Model):
    ingredient = ForeignKey(
        verbose_name="ингредиенты рецепта",
        to=Ingredient,
        on_delete=PROTECT,
        null=False,
    )
    quantity = IntegerField(
        verbose_name="количество",
        null=False,
    )
    unit = ForeignKey(
        verbose_name="единица измерения",
        to=Unit,
        on_delete=PROTECT,
        null=False,
    )

    class Meta:
        verbose_name = "Ингредиенты рецепта"
        verbose_name_plural = "Ингредиенты рецептов"


class Recipe(Model):
    # author_id = 
    name = CharField(
        verbose_name="рецепт",
        max_length=MAX_LEN_RECIPE_CHARFIELD,
    )
    picture = CharField(
        verbose_name="картинка",
        max_length=MAX_LEN_PICTURE_CHARFIELD,
    )
    description = TextField(
        verbose_name="описание",

    )
    ingredient = ForeignKey(
        verbose_name="ингредиент",
        to=RecipeIngredient,
        on_delete=PROTECT,
        null=False,
    )
    tag = ForeignKey(
        verbose_name="тэг",
        to=Tag,
        on_delete=PROTECT,
        null=True,
    )
    cooking_time = IntegerField(
        verbose_name="время приготовления",
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"