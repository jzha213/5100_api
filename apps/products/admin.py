from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage, ProductSpecification, ProductReview


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """分类管理"""
    list_display = ('name', 'parent', 'sort_order', 'is_active', 'icon_preview', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('sort_order', 'name')
    fields = ('name', 'parent', 'icon_file', 'icon', 'icon_preview', 'description', 'sort_order', 'is_active', 'is_deleted', 'created_at', 'updated_at')
    readonly_fields = ('icon_preview', 'created_at', 'updated_at')
    
    def icon_preview(self, obj):
        """图标预览"""
        if obj.icon_file:
            # 如果有上传的文件，优先显示文件
            return format_html(
                '<img src="{}" style="max-height: 80px; max-width: 80px; border: 1px solid #ddd; border-radius: 4px; object-fit: contain;" />', 
                obj.icon_file.url
            )
        elif obj.icon:
            # 如果有 URL，显示 URL 的图片
            return format_html(
                '<img src="{}" style="max-height: 80px; max-width: 80px; border: 1px solid #ddd; border-radius: 4px; object-fit: contain;" />', 
                obj.icon
            )
        return format_html('<span style="color: #999;">无图标</span>')
    icon_preview.short_description = "图标预览"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """商品管理"""
    list_display = ('name', 'sku', 'category', 'price', 'stock', 'is_active', 'created_at')
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('name', 'sku', 'description')
    ordering = ('-created_at',)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """商品图片管理"""
    list_display = ('product', 'alt_text', 'sort_order', 'is_primary', 'image_preview', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('product__name', 'alt_text')
    fields = ('product', 'image_file', 'image_url', 'alt_text', 'sort_order', 'is_primary', 'image_preview')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        """图片预览"""
        if obj.image_file:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image_file.url)
        elif obj.image_url:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image_url)
        return "无图片"
    image_preview.short_description = "图片预览"


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    """商品规格管理"""
    list_display = ('product', 'name', 'value', 'sort_order')
    search_fields = ('product__name', 'name', 'value')


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    """商品评价管理"""
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username')