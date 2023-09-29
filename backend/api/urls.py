from api.views import (
    BaseAPIRootView,
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet,
    UserViewSet,
)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = "api"


class RuDefaultRouter(DefaultRouter):
    """
    Роутер для API с поддержкой кастомного APIRootView.

    Использует кастомное представление APIRootView
    `BaseAPIRootView` вместо стандартного.
    """

    APIRootView = BaseAPIRootView


router = RuDefaultRouter()
router.register("tags", TagViewSet, "tags")
router.register("ingredients", IngredientViewSet, "ingredients")
router.register("recipes", RecipeViewSet, "recipes")
router.register("users", UserViewSet, "users")

urlpatterns = (
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
)

urlpatterns += [
    path(
        "recipes/<int:pk>/favorite/",
        RecipeViewSet.as_view({"post": "recipe_to_favorites"}),
        name="recipe-to-favorites"
    ),
    path(
        "recipes/<int:pk>/favorite/",
        RecipeViewSet.as_view({"delete": "remove_recipe_from_favorites"}),
        name="remove-recipe-from-favorites"
    ),
]
