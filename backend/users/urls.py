# backend/users/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MeViewSet, UserRegistrationView

router = DefaultRouter()
router.register(r'me', MeViewSet, basename='me')
router.register(r'register', UserRegistrationView, basename='register')

urlpatterns = [
    path('', include(router.urls)),
]