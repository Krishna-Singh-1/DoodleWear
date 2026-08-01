from django.contrib import admin
from .models import (
    Design, CustomOrder, ShippingAddress, PaymentDetails,
    Category, Product, Cart, CartItem, 
    RegularOrder, RegularOrderItem, RegularOrderShipping, RegularOrderPayment
)

@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']

@admin.register(CustomOrder)
class CustomOrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer_name', 'customer_email', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at', 'clothing_type']
    search_fields = ['customer_name', 'customer_email', 'order_id']
    readonly_fields = ['order_id', 'created_at', 'updated_at']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock_quantity', 'is_active', 'is_featured']
    list_filter = ['category', 'is_active', 'is_featured']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(RegularOrder)
class RegularOrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer_name', 'customer_email', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer_name', 'customer_email', 'order_id']
