from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django.db.models import QuerySet
from recipes.models import Recipe
from api.serializers import (
    RecipeSerializer,
)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()  # .select_related("author")
    serializer_class = RecipeSerializer

    # def get_queryset(self) -> QuerySet[Recipe]:
    #     queryset = self.queryset

        # tags: list = self.request.query_params.getlist(UrlQueries.TAGS.value)
        # tags: list = self.request.query_params.getlist('tags')
        # if tags:
        #     queryset = queryset.filter(tags__slug__in=tags).distinct()

        # author: str = self.request.query_params.get(UrlQueries.AUTHOR.value)
        # if author:
        #     queryset = queryset.filter(author=author)

        # return queryset
