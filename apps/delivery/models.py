from django.db import models
from apps.common.models import BaseModel
import uuid
from datetime import datetime


class DeliveryPerson(BaseModel):
    """配送员模型"""
    STATUS_CHOICES = [
        (0, '离线'),
        (1, '在线'),
        (2, '忙碌'),
        (3, '休假'),
    ]
    
    # 基本信息
    name = models.CharField('姓名', max_length=50)
    phone = models.CharField('手机号', max_length=20, unique=True)
    id_card = models.CharField('身份证号', max_length=18, blank=True)
    
    # 状态信息
    status = models.SmallIntegerField('状态', choices=STATUS_CHOICES, default=0)
    is_active = models.BooleanField('是否启用', default=True)
    
    # 统计信息
    total_orders = models.IntegerField('总订单数', default=0)
    completed_orders = models.IntegerField('完成订单数', default=0)
    rating = models.DecimalField('评分', max_digits=3, decimal_places=2, default=5.0)
    
    # 位置信息
    current_latitude = models.DecimalField('当前位置纬度', max_digits=10, decimal_places=7, blank=True, null=True)
    current_longitude = models.DecimalField('当前位置经度', max_digits=10, decimal_places=7, blank=True, null=True)
    last_update_location = models.DateTimeField('最后更新位置时间', blank=True, null=True)
    
    class Meta:
        db_table = 'delivery_deliveryperson'
        verbose_name = '配送员'
        verbose_name_plural = '配送员'
        indexes = [
            models.Index(fields=['phone']),
            models.Index(fields=['status']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.phone}"


class Delivery(BaseModel):
    """配送记录模型"""
    STATUS_CHOICES = [
        ('pending', '待分配'),
        ('assigned', '已分配'),
        ('accepted', '已接单'),
        ('picked_up', '已取货'),
        ('delivering', '配送中'),
        ('delivered', '已送达'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]
    
    # 基本信息
    delivery_no = models.CharField('配送单号', max_length=32, unique=True)
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='delivery')
    
    # 配送员信息
    delivery_person = models.ForeignKey(DeliveryPerson, on_delete=models.CASCADE, related_name='deliveries', blank=True, null=True)
    
    # 配送信息
    status = models.CharField('配送状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # 地址信息
    delivery_address = models.TextField('配送地址')
    contact_name = models.CharField('联系人', max_length=50)
    contact_phone = models.CharField('联系电话', max_length=20)
    
    # 详细地址信息
    province = models.CharField('省份', max_length=50, blank=True)
    city = models.CharField('城市', max_length=50, blank=True)
    district = models.CharField('区县', max_length=50, blank=True)
    street = models.CharField('街道', max_length=100, blank=True)
    detail_address = models.CharField('详细地址', max_length=200, blank=True)
    
    # 时间信息
    assigned_at = models.DateTimeField('分配时间', blank=True, null=True)
    accepted_at = models.DateTimeField('接单时间', blank=True, null=True)
    picked_up_at = models.DateTimeField('取货时间', blank=True, null=True)
    delivered_at = models.DateTimeField('送达时间', blank=True, null=True)
    completed_at = models.DateTimeField('完成时间', blank=True, null=True)
    
    # 其他信息
    remark = models.TextField('配送备注', blank=True)
    
    class Meta:
        db_table = 'delivery_delivery'
        verbose_name = '配送记录'
        verbose_name_plural = '配送记录'
        indexes = [
            models.Index(fields=['delivery_no']),
            models.Index(fields=['order']),
            models.Index(fields=['delivery_person']),
            models.Index(fields=['status']),
        ]
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        """保存时自动生成配送单号"""
        if not self.delivery_no:
            # 生成唯一的配送单号：DEL + 时间戳 + 随机字符串
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            random_str = str(uuid.uuid4())[:8].upper()
            self.delivery_no = f"DEL{timestamp}{random_str}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"配送单{self.delivery_no} - {self.order.order_no}"


class DeliveryTrack(BaseModel):
    """配送轨迹模型"""
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name='tracks')
    status = models.CharField('状态', max_length=20)
    latitude = models.DecimalField('纬度', max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField('经度', max_digits=10, decimal_places=7, blank=True, null=True)
    address = models.CharField('地址', max_length=200, blank=True)
    remark = models.TextField('备注', blank=True)
    
    class Meta:
        db_table = 'delivery_deliverytrack'
        verbose_name = '配送轨迹'
        verbose_name_plural = '配送轨迹'
        indexes = [
            models.Index(fields=['delivery', 'created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.delivery.delivery_no} - {self.status} - {self.created_at}"


class DeliveryRating(BaseModel):
    """配送评价模型"""
    RATING_CHOICES = [
        (1, '1星'),
        (2, '2星'),
        (3, '3星'),
        (4, '4星'),
        (5, '5星'),
    ]
    
    delivery = models.OneToOneField(Delivery, on_delete=models.CASCADE, related_name='rating')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='delivery_ratings')
    delivery_person = models.ForeignKey(DeliveryPerson, on_delete=models.CASCADE, related_name='ratings')
    
    # 评价信息
    rating = models.SmallIntegerField('评分', choices=RATING_CHOICES)
    content = models.TextField('评价内容', blank=True)
    
    class Meta:
        db_table = 'delivery_deliveryrating'
        verbose_name = '配送评价'
        verbose_name_plural = '配送评价'
        indexes = [
            models.Index(fields=['delivery']),
            models.Index(fields=['user']),
            models.Index(fields=['delivery_person']),
        ]
    
    def __str__(self):
        return f"{self.delivery.delivery_no} - {self.rating}星评价"
