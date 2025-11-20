from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import User, UserProfile, UserLoginLog


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """用户管理"""
    list_display = ('username', 'email', 'phone', 'nickname', 'avatar_preview', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email', 'phone', 'nickname')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('nickname', 'avatar_url', 'avatar_preview', 'email', 'phone')}),
        ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('重要日期', {'fields': ('last_login', 'date_joined')}),
    )
    
    readonly_fields = ('date_joined', 'last_login', 'avatar_preview')
    
    def avatar_preview(self, obj):
        """头像预览"""
        if obj.avatar_url:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;" />',
                obj.avatar_url
            )
        return "无头像"
    avatar_preview.short_description = "头像预览"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """用户资料管理"""
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__nickname')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(UserLoginLog)
class UserLoginLogAdmin(admin.ModelAdmin):
    """用户登录日志管理"""
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)