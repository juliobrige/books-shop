# backend/users/views.py

from rest_framework import viewsets, status, permissions,  mixins 
from rest_framework.response import Response
from django.contrib.auth.models import User 
from .serializers import UserSerializer, UserRegistrationSerializer

# ... a sua MeViewSet existente ...
class MeViewSet(viewsets.ViewSet):
    """
    View para um utilizador ver e editar o seu próprio perfil.
    """
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRegistrationView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.none() 
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny] # Qualquer pessoa pode se registar

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Opcional: pode-se retornar um token JWT aqui para login automático
        return Response(
            {"detail": f"Utilizador {user.username} criado com sucesso."},
            status=status.HTTP_201_CREATED
        )