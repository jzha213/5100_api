from django.contrib import admin
from .models import Order, OrderItem, Cart, OrderStatusLog


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """订单管理"""
    list_display = ('order_no', 'user', 'total_amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('order_no', 'user__username')
    ordering = ('-created_at',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """订单项管理"""
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__order_no', 'product__name')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """购物车管理"""
    list_display = ('user', 'product', 'quantity', 'created_at')
    search_fields = ('user__username', 'product__name')


@admin.register(OrderStatusLog)
class OrderStatusLogAdmin(admin.ModelAdmin):
    """订单状态日志管理"""
    list_display = ('order', 'created_at')
    search_fields = ('order__order_no',)