# api/exceptions.py

from rest_framework.views import exception_handler
from rest_framework.exceptions import PermissionDenied, NotAuthenticated

def custom_exception_handler(exc, context):
    # Получаем стандартный ответ DRF
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, PermissionDenied):
            # Заменяем сообщение на русское
            response.data['detail'] = 'У вас нет прав для выполнения этого действия.'
        elif isinstance(exc, NotAuthenticated):
            response.data['detail'] = 'Вы не аутентифицированы. Пожалуйста, войдите в систему.'

    return response
