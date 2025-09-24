from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsInstructorOrReadOnly(BasePermission):
    """
    - GET/HEAD/OPTIONS: liberado
    - POST/PUT/PATCH/DELETE: só para usuário com is_instructor=True
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and getattr(request.user, "is_instructor", False))
