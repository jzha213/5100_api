from django.db import models
from apps.common.models import BaseModel


class Coupon(BaseModel):
    """优惠券模型"""
    COUPON_TYPE_CHOICES = [
        ('discount', '折扣券'),
        ('cash', '现金券'),
        ('free_shipping', '免运费券'),
    ]
    
    # 基本信息
    name = models.CharField('优惠券名称', max_length=100)
    description = models.TextField('优惠券描述', blank=True)
    coupon_type = models.CharField('优惠券类型', max_length=20, choices=COUPON_TYPE_CHOICES)
    
    # 优惠信息
    discount_value = models.DecimalField('优惠金额', max_digits=10, decimal_places=2, default=0)
    discount_rate = models.DecimalField('折扣率', max_digits=5, decimal_places=2, blank=True, null=True)
    min_amount = models.DecimalField('最低消费金额', max_digits=10, decimal_places=2, default=0)
    max_discount = models.DecimalField('最大优惠金额', max_digits=10, decimal_places=2, blank=True, null=True)
    
    # 使用条件
    total_count = models.IntegerField('发放总数', default=0)
    used_count = models.IntegerField('已使用数量', default=0)
    per_user_limit = models.IntegerField('每用户限领数量', default=1)
    
    # 时间限制
    valid_from = models.DateTimeField('有效期开始时间')
    valid_to = models.DateTimeField('有效期结束时间')
    
    # 适用范围
    applicable_products = models.ManyToManyField('products.Product', blank=True, related_name='applicable_coupons')
    applicable_categories = models.ManyToManyField('products.Category', blank=True, related_name='applicable_coupons')
    
    # 状态
    is_active = models.BooleanField('是否启用', default=True)
    
    class Meta:
        db_table = 'coupons_coupon'
        verbose_name = '优惠券'
        verbose_name_plural = '优惠券'
        indexes = [
            models.Index(fields=['coupon_type']),
            models.Index(fields=['is_active']),
            models.Index(fields=['valid_from', 'valid_to']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def is_valid(self):
        """是否有效"""
        from django.utils import timezone
        now = timezone.now()
        return self.is_active and self.valid_from <= now <= self.valid_to and self.used_count < self.total_count


class UserCoupon(BaseModel):
    """用户优惠券模型"""
    STATUS_CHOICES = [
        ('unused', '未使用'),
        ('used', '已使用'),
        ('expired', '已过期'),
    ]
    
    # 基本信息
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='coupons')
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='user_coupons')
    
    # 使用信息
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='unused')
    used_at = models.DateTimeField('使用时间', blank=True, null=True)
    used_order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, blank=True, null=True, related_name='used_coupons')
    
    # 过期时间
    expired_at = models.DateTimeField('过期时间')
    
    class Meta:
        db_table = 'coupons_usercoupon'
        verbose_name = '用户优惠券'
        verbose_name_plural = '用户优惠券'
        unique_together = ['user', 'coupon']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['coupon']),
            models.Index(fields=['expired_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.nickname} - {self.coupon.name}"
    
    @property
    def is_expired(self):
        """是否过期"""
        from django.utils import timezone
        return timezone.now() > self.expired_at


class CouponUsage(BaseModel):
    """优惠券使用记录模型"""
    user_coupon = models.ForeignKey(UserCoupon, on_delete=models.CASCADE, related_name='usage_records')
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='coupon_usages')
    discount_amount = models.DecimalField('优惠金额', max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'coupons_couponusage'
        verbose_name = '优惠券使用记录'
        verbose_name_plural = '优惠券使用记录'
        indexes = [
            models.Index(fields=['user_coupon']),
            models.Index(fields=['order']),
        ]
    
    def __str__(self):
        return f"{self.user_coupon} - 优惠{self.discount_amount}元"
