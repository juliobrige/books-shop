# backend/users/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MeViewSet

# 1. Cria um router
router = DefaultRouter()

# 2. Regista a sua ViewSet com o router
# O router vai criar o URL 'me/' para nós.
# 'basename' é importante para ajudar o router a nomear as rotas.
router.register(r'me', MeViewSet, basename='me')

# 3. As URLs são geradas automaticamente
urlpatterns = [
    path('', include(router.urls)),
]