from django.contrib.auth import get_user_model
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q, QuerySet
from django.http.response import HttpResponse
from djoser.views import UserViewSet as DjoserUserViewSet
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.routers import APIRootView
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.mixins import AddDelViewMixin
from api.paginators import PageLimitPagination
from api.permissions import AdminOrReadOnly, AuthorStaffOrReadOnly
from api.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    ShortRecipeSerializer,
    TagSerializer,
    UserSubscribeSerializer,
)
from core.enums import Tuples, UrlQueries
from core.services import create_shoping_list
from recipes.models import Carts, Favorites, Ingredient, Recipe, Tag
from users.models import Subscriptions


User = get_user_model()


class BaseAPIRootView(APIRootView):
    """
    Базовый класс для корневой точки API.
    """


class UserViewSet(DjoserUserViewSet, AddDelViewMixin):
    """
    Вьюсет для пользователей.
    """

    pagination_class = PageLimitPagination
    permission_classes = (DjangoModelPermissions,)
    add_serializer = UserSubscribeSerializer
    link_model = Subscriptions

    def create_subscribe(
        self, request: WSGIRequest, id: int | str
    ) -> Response:
        return self._create_relation(id)

    def delete_subscribe(
        self, request: WSGIRequest, id: int | str
    ) -> Response:
        """
        Удаление подписки на пользователя.
        """
        return self._delete_relation(Q(author__id=id))

    @action(
        methods=("get",), detail=False, permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request: WSGIRequest) -> Response:
        """
        Получение списка подписок пользователя.
        """
        pages = self.paginate_queryset(
            User.objects.filter(subscribers__user=self.request.user)
        )
        serializer = UserSubscribeSerializer(pages, many=True)
        return self.get_paginated_response(serializer.data)


class TagViewSet(ReadOnlyModelViewSet):
    """
    Вьюсет для тегов.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOrReadOnly,)


class IngredientFilter(filters.FilterSet):
    search_name = filters.CharFilter(
        field_name="name", lookup_expr="icontains")

    class Meta:
        model = Ingredient
        fields = ["search_name"]


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AdminOrReadOnly,)
    filterset_class = IngredientFilter


class RecipeViewSet(ModelViewSet, AddDelViewMixin):
    """
    Вьюсет для рецептов.
    """
    queryset = Recipe.objects.select_related("author")
    serializer_class = RecipeSerializer
    permission_classes = (AuthorStaffOrReadOnly,)
    pagination_class = PageLimitPagination
    add_serializer = ShortRecipeSerializer

    def get_queryset(self) -> QuerySet[Recipe]:
        """
        Получение списка рецептов с учетом фильтров.
        """
        queryset = self.queryset

        tags: list = self.request.query_params.getlist(UrlQueries.TAGS.value)
        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()

        author: str = self.request.query_params.get(UrlQueries.AUTHOR.value)
        if author:
            queryset = queryset.filter(author=author)

        # фильтры для авторизованного пользователя
        if self.request.user.is_anonymous:
            return queryset

        is_in_cart: str = self.request.query_params.get(UrlQueries.SHOP_CART)
        if is_in_cart in Tuples.SYMBOL_TRUE_SEARCH.value:
            queryset = queryset.filter(in_carts__user=self.request.user)
        elif is_in_cart in Tuples.SYMBOL_FALSE_SEARCH.value:
            queryset = queryset.exclude(in_carts__user=self.request.user)

        is_favorite: str = self.request.query_params.get(UrlQueries.FAVORITE)
        if is_favorite in Tuples.SYMBOL_TRUE_SEARCH.value:
            queryset = queryset.filter(in_favorites__user=self.request.user)
        if is_favorite in Tuples.SYMBOL_FALSE_SEARCH.value:
            queryset = queryset.exclude(in_favorites__user=self.request.user)

        return queryset

    def recipe_to_favorites(
        self, request: WSGIRequest, pk: int | str
    ) -> Response:
        self.link_model = Favorites
        return self._create_relation(pk)

    def remove_recipe_from_favorites(
        self, request: WSGIRequest, pk: int | str
    ) -> Response:
        self.link_model = Favorites
        return self._delete_relation(Q(recipe__id=pk))

    @action(detail=True, permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request: WSGIRequest, pk: int | str) -> Response:
        """
        Добавление рецепта в корзину покупок пользователя.

        Args:
            request (WSGIRequest): Запрос от клиента.
            pk (int | str): Идентификатор рецепта,
            который нужно добавить в корзину.

        Returns:
            Response: Ответ сервера,
            обычно с информацией об успешном добавлении.

        """

    @shopping_cart.mapping.post
    def recipe_to_cart(self, request: WSGIRequest, pk: int | str) -> Response:
        self.link_model = Carts
        return self._create_relation(pk)

    @shopping_cart.mapping.delete
    def remove_recipe_from_cart(
        self, request: WSGIRequest, pk: int | str
    ) -> Response:
        self.link_model = Carts
        return self._delete_relation(Q(recipe__id=pk))

    @action(methods=("get",), detail=False)
    def download_shopping_cart(self, request: WSGIRequest) -> Response:
        """
        Метод для конкретной реализации добавления рецепта в корзину.

        Args:
            request (WSGIRequest): Запрос от клиента.
            pk (int | str): Идентификатор рецепта,
            который нужно добавить в корзину.

        Returns:
            Response: Ответ сервера, обычно с
            информацией об успешном добавлении.

        """
        user = self.request.user
        if not user.carts.exists():
            return Response(status=HTTP_400_BAD_REQUEST)

        filename = f"{user.username}_shopping_list.txt"
        shopping_list = create_shoping_list(user)
        response = HttpResponse(
            shopping_list, content_type="text.txt; charset=utf-8"
        )
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response
