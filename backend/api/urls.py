from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BookViewSet, AuthorViewSet, CategoryViewSet,
    CartViewSet, OrderViewSet
)

router = DefaultRouter()
router.register(r"books", BookViewSet, basename="book")
router.register(r"authors", AuthorViewSet, basename="author")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns = [
    path("", include(router.urls)),
    path("cart/", CartViewSet.as_view({"get":"list"}), name="cart"),
    path("cart/add/", CartViewSet.as_view({"post":"add_item"}), name="cart-add"),
    path("cart/remove/", CartViewSet.as_view({"post":"remove_item"}), name="cart-remove"),
    path("cart/clear/", CartViewSet.as_view({"post":"clear"}), name="cart-clear"),
    path("cart/checkout/", CartViewSet.as_view({"post":"checkout"}), name="cart-checkout"),
]
