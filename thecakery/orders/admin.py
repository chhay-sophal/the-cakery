from django.contrib import admin
from .models import *

# Register the Cart model
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at', 'total_price')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at', 'total_price')

    def total_price(self, obj):
        return obj.total_price()

# Register the CartItem model
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'content_object', 'quantity', 'size', 'get_price', 'custom_text')
    search_fields = ('cart__user__username', 'custom_text')
    list_filter = ('cart__user',)
    
    def content_object(self, obj):
        return str(obj.content_object)

    def get_price(self, obj):
        return obj.get_price()
    get_price.short_description = 'Price'

# Register the Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'shipping_status', 'payment_status', 'created_at')
    search_fields = ('user__username', 'destination')
    list_filter = ('shipping_status', 'payment_status', 'created_at')
    readonly_fields = ('created_at', 'updated_at', 'calculate_total_price')

    def total_price(self, obj):
        return obj.calculate_total_price()

# Register the OrderItem model
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'content_object', 'quantity')
    search_fields = ('order__user__username',)

    def content_object(self, obj):
        return str(obj.content_object)