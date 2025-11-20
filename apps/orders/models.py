from django.db import models
from django.utils import timezone
from apps.common.models import BaseModel
import uuid


class Order(BaseModel):
    """订单模型"""
    STATUS_CHOICES = [
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('confirmed', '已确认'),
        ('preparing', '备货中'),
        ('shipping', '配送中'),
        ('delivered', '已送达'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
        ('refunded', '已退款'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('unpaid', '未支付'),
        ('paid', '已支付'),
        ('refunding', '退款中'),
        ('refunded', '已退款'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('wechat', '微信支付'),
        ('alipay', '支付宝'),
        ('balance', '余额支付'),
    ]
    
    # 订单基本信息
    order_no = models.CharField('订单号', max_length=32, unique=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='orders')
    
    # 订单状态
    status = models.CharField('订单状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # 金额信息
    total_amount = models.DecimalField('订单总金额', max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField('优惠金额', max_digits=10, decimal_places=2, default=0)
    shipping_fee = models.DecimalField('配送费', max_digits=10, decimal_places=2, default=0)
    final_amount = models.DecimalField('实付金额', max_digits=10, decimal_places=2)
    
    # 支付信息
    payment_method = models.CharField('支付方式', max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True)
    payment_status = models.CharField('支付状态', max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    payment_time = models.DateTimeField('支付时间', blank=True, null=True)
    
    # 配送信息
    delivery_time = models.DateTimeField('配送时间', blank=True, null=True)
    completed_time = models.DateTimeField('完成时间', blank=True, null=True)
    
    # 其他信息
    cancel_reason = models.TextField('取消原因', blank=True)
    remark = models.TextField('订单备注', blank=True)
    
    class Meta:
        db_table = 'orders_order'
        verbose_name = '订单'
        verbose_name_plural = '订单'
        indexes = [
            models.Index(fields=['order_no']),
            models.Index(fields=['user']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"订单{self.order_no} - {self.user.nickname}"
    
    def save(self, *args, **kwargs):
        if not self.order_no:
            self.order_no = self.generate_order_no()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_order_no():
        """生成订单号"""
        return f"WD{timezone.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4())[:6].upper()}"


class OrderItem(BaseModel):
    """订单商品模型"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    
    # 商品快照信息
    product_name = models.CharField('商品名称', max_length=200)
    product_image = models.URLField('商品图片', blank=True)
    product_sku = models.CharField('商品SKU', max_length=100)
    
    # 价格和数量
    price = models.DecimalField('商品价格', max_digits=10, decimal_places=2)
    quantity = models.IntegerField('数量')
    subtotal = models.DecimalField('小计', max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'orders_orderitem'
        verbose_name = '订单商品'
        verbose_name_plural = '订单商品'
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['product']),
        ]
    
    def __str__(self):
        return f"{self.order.order_no} - {self.product_name} x{self.quantity}"


class Cart(BaseModel):
    """购物车模型"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField('数量', default=1)
    address = models.ForeignKey('addresses.Address', on_delete=models.CASCADE, null=True, blank=True, verbose_name='收货地址')
    notes = models.TextField('备注', blank=True, null=True)
    
    class Meta:
        db_table = 'orders_cart'
        verbose_name = '购物车'
        verbose_name_plural = '购物车'
        # 移除 unique_together，允许相同商品不同地址的购物车项目
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['product']),
            models.Index(fields=['address']),
        ]
    
    def __str__(self):
        return f"{self.user.nickname} - {self.product.name} x{self.quantity}"
    
    @property
    def subtotal(self):
        """小计"""
        return self.product.price * self.quantity


class OrderStatusLog(BaseModel):
    """订单状态变更日志"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_logs')
    from_status = models.CharField('原状态', max_length=20, blank=True)
    to_status = models.CharField('新状态', max_length=20)
    operator = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=True, null=True)
    remark = models.TextField('备注', blank=True)
    
    class Meta:
        db_table = 'orders_orderstatuslog'
        verbose_name = '订单状态日志'
        verbose_name_plural = '订单状态日志'
        indexes = [
            models.Index(fields=['order', 'created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.order.order_no} - {self.from_status} -> {self.to_status}"
