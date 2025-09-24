# backend/api/admin.py

from django.contrib import admin
from .models import (
    Author, Category, Book,
    Cart, CartItem,
    Order, OrderItem
)

# ---- Configurações Avançadas para o Admin ----

class BookAdmin(admin.ModelAdmin):
    # Campos a serem exibidos na lista de livros
    list_display = ('title', 'category', 'price', 'stock')
    # Filtros que aparecerão na barra lateral direita
    list_filter = ('category', 'authors')
    # Campos pelos quais se pode pesquisar
    search_fields = ('title', 'authors__name')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    # Campos apenas para leitura, pois não devem ser editados aqui
    readonly_fields = ('book', 'quantity', 'unit_price')
    # Impede que se adicione novos itens a um pedido já criado
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total', 'created_at')
    list_filter = ('status', 'created_at')
    # Mostra os itens do pedido dentro da página de detalhes do pedido
    inlines = [OrderItemInline]


# ---- Registo dos Modelos ----

# Modelos simples (sem configuração extra)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)

# Modelos com a configuração personalizada
admin.site.register(Book, BookAdmin)
admin.site.register(Order, OrderAdmin)