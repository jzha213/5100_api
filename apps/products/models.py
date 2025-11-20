from django.db import models
from apps.common.models import BaseModel, SoftDeleteModel


class Category(BaseModel):
    """商品分类模型"""
    name = models.CharField('分类名称', max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    icon = models.URLField('分类图标', blank=True)
    description = models.TextField('分类描述', blank=True)
    sort_order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    
    class Meta:
        db_table = 'products_category'
        verbose_name = '商品分类'
        verbose_name_plural = '商品分类'
        indexes = [
            models.Index(fields=['parent']),
            models.Index(fields=['sort_order']),
            models.Index(fields=['is_active']),
        ]
        ordering = ['sort_order', 'id']
    
    def __str__(self):
        return self.name


class Product(SoftDeleteModel):
    """商品模型"""
    name = models.CharField('商品名称', max_length=200)
    description = models.TextField('商品描述', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    sku = models.CharField('商品SKU', max_length=100, unique=True)
    
    # 价格信息
    price = models.DecimalField('价格', max_digits=10, decimal_places=2)
    original_price = models.DecimalField('原价', max_digits=10, decimal_places=2, blank=True, null=True)
    
    # 库存和销量
    stock = models.IntegerField('库存', default=0)
    sales_count = models.IntegerField('销量', default=0)
    
    # 商品属性
    weight = models.DecimalField('重量(kg)', max_digits=8, decimal_places=2, blank=True, null=True)
    volume = models.DecimalField('体积(L)', max_digits=8, decimal_places=2, blank=True, null=True)
    
    # 图片和规格
    images = models.JSONField('商品图片JSON数组', default=list, blank=True)
    specifications = models.JSONField('规格参数JSON', default=dict, blank=True)
    
    # 状态
    is_active = models.BooleanField('是否启用', default=True)
    is_featured = models.BooleanField('是否推荐', default=False)
    sort_order = models.IntegerField('排序', default=0)
    
    class Meta:
        db_table = 'products_product'
        verbose_name = '商品'
        verbose_name_plural = '商品'
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['sku']),
            models.Index(fields=['price']),
            models.Index(fields=['is_active']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['sort_order']),
        ]
        ordering = ['sort_order', '-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def discount_rate(self):
        """折扣率"""
        if self.original_price and self.original_price > 0:
            return round((self.original_price - self.price) / self.original_price * 100, 1)
        return 0


class ProductImage(BaseModel):
    """商品图片模型"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image_url = models.URLField('图片URL', blank=True, null=True)
    image_file = models.ImageField('图片文件', upload_to='products/images/', blank=True, null=True)
    alt_text = models.CharField('图片描述', max_length=200, blank=True)
    sort_order = models.IntegerField('排序', default=0)
    is_primary = models.BooleanField('是否主图', default=False)
    
    class Meta:
        db_table = 'products_productimage'
        verbose_name = '商品图片'
        verbose_name_plural = '商品图片'
        indexes = [
            models.Index(fields=['product', 'sort_order']),
        ]
        ordering = ['sort_order']
    
    def get_image_url(self):
        """获取图片URL，优先使用本地文件"""
        if self.image_file:
            # 对于小程序，返回相对路径，让小程序自己处理
            from django.conf import settings
            return f"{settings.MEDIA_URL}{self.image_file.name}"
        return self.image_url
    
    def __str__(self):
        return f"{self.product.name} - {self.alt_text}"


class ProductSpecification(BaseModel):
    """商品规格模型"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_specifications')
    name = models.CharField('规格名称', max_length=100)
    value = models.CharField('规格值', max_length=200)
    sort_order = models.IntegerField('排序', default=0)
    
    class Meta:
        db_table = 'products_productspecification'
        verbose_name = '商品规格'
        verbose_name_plural = '商品规格'
        indexes = [
            models.Index(fields=['product', 'sort_order']),
        ]
        ordering = ['sort_order']
    
    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"


class ProductReview(BaseModel):
    """商品评价模型"""
    RATING_CHOICES = [
        (1, '1星'),
        (2, '2星'),
        (3, '3星'),
        (4, '4星'),
        (5, '5星'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='product_reviews')
    rating = models.SmallIntegerField('评分', choices=RATING_CHOICES)
    content = models.TextField('评价内容')
    images = models.JSONField('评价图片', default=list, blank=True)
    is_anonymous = models.BooleanField('是否匿名', default=False)
    
    class Meta:
        db_table = 'products_productreview'
        verbose_name = '商品评价'
        verbose_name_plural = '商品评价'
        indexes = [
            models.Index(fields=['product', 'created_at']),
            models.Index(fields=['user']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.product.name} - {self.user.nickname} - {self.rating}星"
