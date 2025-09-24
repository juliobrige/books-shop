# backend/api/permissions.py

from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permissão personalizada para permitir que apenas administradores (staff)
    editem um objeto. Outros utilizadores têm permissão apenas para leitura.
    """

    def has_permission(self, request, view):
        # Permite pedidos de leitura (GET, HEAD, OPTIONS) a qualquer pessoa.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Permite pedidos de escrita (POST, PUT, DELETE) apenas se o
        # utilizador for staff.
        return request.user and request.user.is_staff