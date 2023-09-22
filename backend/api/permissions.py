from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Model
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.routers import APIRootView


class BanPermission(BasePermission):
    """
    Разрешение для ограничения доступа на основе аутентификации и методов HTTP.

    Разрешает доступ к представлениям только для
    аутентифицированных пользователей, если они активны,
    или для безопасных HTTP-методов (GET, HEAD, OPTIONS).
    """

    def has_permission(self, request: WSGIRequest, view: APIRootView) -> bool:
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
        )


class AuthorStaffOrReadOnly(BanPermission):
    """
    Разрешение для доступа к объектам, ограниченное по аутентификации и ролям.

    Разрешает доступ к объектам только для
    аутентифицированных пользователей, если они активны,
    или для безопасных HTTP-методов (GET, HEAD, OPTIONS).
    Дополнительно разрешает доступ для авторов объектов или сотрудников
    (пользователей со статусом "staff").
    """

    def has_object_permission(
        self, request: WSGIRequest, view: APIRootView, obj: Model
    ) -> bool:
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
            and (request.user == obj.author or request.user.is_staff)
        )


class AdminOrReadOnly(BanPermission):
    """
    Разрешение для доступа к объектам администраторам или только для чтения.

    Разрешает доступ к объектам только для
    аутентифицированных пользователей, если они активны,
    или для безопасных HTTP-методов (GET, HEAD, OPTIONS).
    Дополнительно разрешает доступ только для пользователей
    с ролью "staff" (сотрудников).
    """

    def has_object_permission(
        self, request: WSGIRequest, view: APIRootView
    ) -> bool:
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
            and request.user.is_staff
        )


class OwnerUserOrReadOnly(BanPermission):
    """
    Разрешение для доступа к объектам владельцам,
    администраторам или только для чтения.

    Разрешает доступ к объектам только для
    аутентифицированных пользователей, если они активны,
    или для безопасных HTTP-методов (GET, HEAD, OPTIONS).
    Дополнительно разрешает доступ только для владельцев объектов,
    администраторов или пользователей с ролью "staff" (сотрудников).
    """

    def has_object_permission(
        self, request: WSGIRequest, view: APIRootView, obj: Model
    ) -> bool:
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
            and (request.user == obj.author or request.user.is_staff)
        )
