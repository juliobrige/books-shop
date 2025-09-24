from rest_framework import serializers
from .models import Author, Category, Book, Cart, CartItem, Order, OrderItem

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "bio"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]

class BookSerializer(serializers.ModelSerializer):
    # Opcional: melhora a representação dos campos de chave estrangeira
    category = CategorySerializer(read_only=True)
    authors = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        # '__all__' irá automaticamente incluir os novos campos `cover_image` e `book_file`
        fields = '__all__'


# --------- Carrinho & Pedidos ---------

class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["book", "quantity"]

class CartItemSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source="book.title", read_only=True)
    price = serializers.DecimalField(source="book.price", max_digits=9, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "book", "book_title", "quantity", "price"]

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "is_active", "created_at", "items"]

class OrderItemSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source="book.title", read_only=True)
    line_total = serializers.SerializerMethodField()

    def get_line_total(self, obj):
        return obj.quantity * obj.unit_price

    class Meta:
        model = OrderItem
        fields = ["id", "book", "book_title", "quantity", "unit_price", "line_total"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "status", "total", "created_at", "items"]
