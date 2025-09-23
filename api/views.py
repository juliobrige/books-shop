from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend   # <<< IMPORT QUE FALTA
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import transaction
from .models import Book, Author, Category, Cart, CartItem, Order, OrderItem
from .serializers import (
    BookSerializer, AuthorSerializer, CategorySerializer,
    CartSerializer, CartItemSerializer, CartItemCreateSerializer,
    OrderSerializer
)

class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.select_related("category").prefetch_related("authors").order_by("-created_at")
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category__slug"]
    search_fields = ["title", "description", "authors__name"]
    ordering_fields = ["price", "title", "created_at"]

class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.all().order_by("name")
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=["post"], url_path="add")
    def add_item(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)
        serializer = CartItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.validated_data["book"]
        qty = serializer.validated_data.get("quantity", 1)
        item, created = CartItem.objects.get_or_create(cart=cart, book=book, defaults={"quantity": qty})
        if not created:
            item.quantity += qty
            item.save()
        return Response(CartSerializer(cart).data, status=201)

    @action(detail=False, methods=["post"], url_path="remove")
    def remove_item(self, request):
        cart = Cart.objects.filter(user=request.user, is_active=True).first()
        if not cart:
            return Response({"detail": "Carrinho vazio."}, status=400)
        book_id = request.data.get("book")
        try:
            item = cart.items.get(book_id=book_id)
        except CartItem.DoesNotExist:
            return Response({"detail": "Item não está no carrinho."}, status=404)
        item.delete()
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=["post"], url_path="clear")
    def clear(self, request):
        cart = Cart.objects.filter(user=request.user, is_active=True).first()
        if not cart:
            return Response({"detail": "Carrinho já está vazio."})
        cart.items.all().delete()
        return Response(CartSerializer(cart).data)

    @transaction.atomic
    @action(detail=False, methods=["post"], url_path="checkout")
    def checkout(self, request):
        cart = Cart.objects.select_for_update().filter(user=request.user, is_active=True).first()
        if not cart or cart.items.count() == 0:
            return Response({"detail": "Carrinho vazio."}, status=400)

        order = Order.objects.create(user=request.user, status="PENDING", total=0)
        total = 0
        for it in cart.items.select_related("book"):
            unit = it.book.price
            OrderItem.objects.create(order=order, book=it.book, quantity=it.quantity, unit_price=unit)
            total += float(unit) * it.quantity
        order.total = total
        order.status = "PAID"   # mock: considere integrar com gateway depois
        order.save()

        cart.is_active = False
        cart.save()

        return Response(OrderSerializer(order).data, status=201)

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items__book")    
