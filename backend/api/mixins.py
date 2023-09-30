from django.db.models import Model, Q
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)


class AddDelViewMixin:
    """
    Миксин для добавления и удаления связей между объектами.
    """

    add_serializer: ModelSerializer | None = None
    link_model: Model | None = None

    def _create_relation(self, obj_id: int | str, context=None) -> Response:
        """
        Создает связь между объектами.

        Args:
            obj_id (int | str): Идентификатор объекта.
            context: Контекст запроса.

        Returns:
            Response: Ответ API с данными о созданной связи.
        """
        obj = get_object_or_404(self.queryset, pk=obj_id)
        try:
            self.link_model(None, obj.pk, context['request'].user.pk).save()
        except IntegrityError:
            return Response(
                {"error": "Действие уже выполнено ранее."},
                status=HTTP_400_BAD_REQUEST,
            )

        serializer: ModelSerializer = self.add_serializer(obj, context=context)
        return Response(serializer.data, status=HTTP_201_CREATED)

    def _delete_relation(self, q: Q, context=None) -> Response:
        """
        Удаляет связь между объектами.

        Args:
            q (Q): Условие для поиска связи.
            context: Контекст запроса.

        Returns:
            Response: Ответ API об успешном удалении связи.
        """
        deleted, _ = (
            self.link_model.objects.filter(q & Q(user=context['request'].user))
            .first()
            .delete()
        )
        if not deleted:
            return Response(
                {"error": f"{self.link_model.__name__} не существует"},
                status=HTTP_400_BAD_REQUEST,
            )

        return Response(status=HTTP_204_NO_CONTENT)
