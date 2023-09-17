from django.db import models
from recipes.models import Recipe
from django.db.models import (
    ForeignKey,
    SET_NULL
)
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    # subscriptions = ForeignKey(
    #     verbose_name="подписки",
    #     to='self',  # Сам на себя
    #     on_delete=SET_NULL,
    #     null=True,
    #     blank=True
    # )
    favorite_recipes = ForeignKey(
        verbose_name="любимый рецепт",
        to=Recipe,
        related_name='user_favorite_recipes',
        on_delete=SET_NULL,
        null=True,
        blank=True
    )
    cart = ForeignKey(
        verbose_name="корзина",
        to=Recipe,
        related_name='user_cart',
        on_delete=SET_NULL,
        null=True,
        blank=True
    )
    own_recipe = ForeignKey(
        verbose_name="мой рецепт",
        to=Recipe,
        related_name='author_id',
        on_delete=SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("username",)

    def __str__(self) -> str:
        return f"{self.username}: {self.email}"
