from rest_framework import permissions

class IsSupplier(permissions.BasePermission):
    """
    Разрешает доступ только пользователям с типом 'supplier'.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == 'supplier'

    def has_object_permission(self, request, view, obj):
        # Дополнительно проверяем, что склад принадлежит текущему пользователю
        return obj.owner == request.user

class IsConsumer(permissions.BasePermission):
    """
    Разрешает доступ только пользователям с типом 'consumer'.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == 'consumer'

    def has_object_permission(self, request, view, obj):
        # Здесь можно добавить дополнительную логику, если необходимо
        return True
