from api.views import (
    RecipeViewSet,
)
from django.urls import include, path
from rest_framework.routers import DefaultRouter


app_name = "api"


router = DefaultRouter(trailing_slash=False)

router.register("recipes", RecipeViewSet, "recipes")


urlpatterns = (
    path("", include(router.urls)),
)
