from django.contrib import admin
from .models import Coupon, UserCoupon, CouponUsage


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    """优惠券管理"""
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')


@admin.register(UserCoupon)
class UserCouponAdmin(admin.ModelAdmin):
    """用户优惠券管理"""
    list_display = ('user', 'coupon', 'created_at')
    search_fields = ('user__username', 'coupon__name')


@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    """优惠券使用记录管理"""
    list_display = ('user_coupon', 'order', 'created_at')
    search_fields = ('user_coupon__user__username', 'order__order_no')