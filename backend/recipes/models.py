from django.db.models import (
    Model,
    CharField,
    ImageField,
    ForeignKey,
    PROTECT,
    DO_NOTHING,
    IntegerField,
    TextField,
    ManyToManyField,
)
from django.contrib.contenttypes.models import ContentType
# from users.models import MyUser


MAX_LEN_TAG_NAME_CHARFIELD = 50
MAX_LEN_TAG_COLOR_CHARFIELD = 7
MAX_LEN_TAG_SLUG_CHARFIELD = 20
MAX_LEN_INGREDIENT_CHARFIELD = 100
MAX_LEN_UNIT_CHARFIELD = 25
MAX_LEN_RECIPE_CHARFIELD = 100
MAX_LEN_PICTURE_CHARFIELD = 255


# models.CASCADE
# models.PROTECT — запрещает удалять пользователя, пока у него есть посты.
# models.SET_NULL — посты останутся в БД даже при удалении автора, но значение в поле author у постов изменится на None.
# models.SET_DEFAULT

class Tag(Model):
    name = CharField(
        verbose_name="название тэга",
        max_length=MAX_LEN_TAG_NAME_CHARFIELD
    )
    color = CharField(
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

    def __str__(self):
        return self.name


class Ingredient(Model):
    name = CharField(
        verbose_name="Ингредиент",
        max_length=MAX_LEN_INGREDIENT_CHARFIELD,
    )
    measurement_unit = CharField(
        verbose_name="Единица измерения",
        max_length=MAX_LEN_UNIT_CHARFIELD,
    )
    amount = IntegerField(
        verbose_name="количество",
        null=False,
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return f'{self.name}, {self.amount} {self.measurement_unit}'


# class RecipeIngredient(Model):
#     ingredient = ForeignKey(
#         verbose_name="ингредиенты рецепта",
#         to=Ingredient,
#         on_delete=PROTECT,
#         null=False,
#     )
    

    # class Meta:
    #     verbose_name = "Ингредиенты рецепта"
    #     verbose_name_plural = "Ингредиенты рецептов"

    # def __str__(self):
    #     return (
    #         self.ingredient.name + ', ' +
    #         self.quantity.__str__() 
    #     )


class Recipe(Model):
    author = ForeignKey(
        verbose_name="автор",
        to='users.Myuser',
        on_delete=DO_NOTHING
    )
    name = CharField(
        verbose_name="рецепт",
        max_length=MAX_LEN_RECIPE_CHARFIELD,
    )
    image = ImageField(
        verbose_name="картинка",
        max_length=MAX_LEN_PICTURE_CHARFIELD,
        blank=True
    )
    description = TextField(
        verbose_name="описание",

    )
    ingredients = ManyToManyField(
        Ingredient,
        verbose_name="ингредиент",
    )
    tags = ManyToManyField(
        Tag,
        verbose_name="тэг",
    )
    cooking_time = IntegerField(
        verbose_name="время приготовления",
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name
