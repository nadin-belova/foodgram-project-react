from datetime import datetime as dt
from typing import TYPE_CHECKING
from urllib.parse import unquote

from django.apps import apps
from django.db.models import F, Sum
from foodgram.settings import DATE_TIME_FORMAT
from recipes.models import AmountIngredient, Recipe

if TYPE_CHECKING:
    from recipes.models import Ingredient
    from users.models import MyUser


def recipe_ingredients_set(
    recipe: Recipe, ingredients: dict[int, tuple["Ingredient", int]]
) -> None:
    """
    Добавляет ингредиенты в рецепт.

    :param recipe: Рецепт, в который добавляются ингредиенты.
    :param ingredients: Словарь с ингредиентами и их количеством.
        Ключи - это ID ингредиентов,
        значения - кортежи (Ингредиент, количество).
    :return: None
    """
    objs = []

    for ingredient, amount in ingredients.values():
        objs.append(
            AmountIngredient(
                recipe=recipe, ingredients=ingredient, amount=amount
            )
        )

    AmountIngredient.objects.bulk_create(objs)


def create_shoping_list(user: "MyUser") -> str:
    """
    Создает список покупок для пользователя.

    :param user: Пользователь, для которого создается список покупок.
    :return: Строка с созданным списком покупок.
    """
    shopping_list = [
        f"Список покупок для:\n\n{user.first_name}\n"
        f"{dt.now().strftime(DATE_TIME_FORMAT)}\n"
    ]
    Ingredient = apps.get_model("recipes", "Ingredient")
    ingredients = (
        Ingredient.objects.filter(recipe__recipe__in_carts__user=user)
        .values("name", measurement=F("measurement_unit"))
        .annotate(amount=Sum("recipe__amount"))
    )
    ing_list = (
        f'{ing["name"]}: {ing["amount"]} {ing["measurement"]}'
        for ing in ingredients
    )
    shopping_list.extend(ing_list)

    shopping_list.append("\nПосчитано в Foodgram")
    return "\n".join(shopping_list)


def maybe_incorrect_layout(url_string: str) -> str:
    """
    Проверяет строку URL на возможно некорректное расположение символов.

    :param url_string: Строка URL для проверки.
    :return: Преобразованная строка URL.
    """
    equals = str.maketrans(
        "qwertyuiop[]asdfghjkl;'zxcvbnm,./",
        "йцукенгшщзхъфывапролджэячсмитьбю.",
    )
    if url_string.startswith("%"):
        return unquote(url_string).lower()

    return url_string.translate(equals).lower()
