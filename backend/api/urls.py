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
router.register(
    r'recipes/(?P<pk>[^/.]+)/favorite',
    RecipeViewSet,
    basename='recipe-favorite'
)
router.register("users", UserViewSet, "users")
router.register(
    r'users/(?P<pk>[^/.]+)/subscribe',
    UserViewSet,
    basename='user-subscribe'
)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
]
