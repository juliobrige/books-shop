# backend/users/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated # <-- IMPORTE ISTO
from .serializers import UserSerializer

class MeViewSet(viewsets.ViewSet):
    """
    View para obter os dados do utilizador autenticado.
    """
    permission_classes = [IsAuthenticated] # <-- ADICIONE ESTA LINHA

    def list(self, request):
        # O `request.user` aqui será o utilizador autenticado, graças ao token
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)