from django.contrib import admin
from .models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """地址管理"""
    list_display = ('user', 'name', 'phone', 'province', 'city', 'is_default', 'created_at')
    list_filter = ('is_default', 'province', 'city', 'created_at')
    search_fields = ('user__username', 'name', 'phone', 'address')
    ordering = ('-created_at',)