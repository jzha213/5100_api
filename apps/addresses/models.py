from django.db import models
from apps.common.models import BaseModel


class Address(BaseModel):
    """用户地址模型"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField('收货人姓名', max_length=50)
    phone = models.CharField('收货人电话', max_length=20)
    
    # 地址信息
    province = models.CharField('省份', max_length=50)
    city = models.CharField('城市', max_length=50)
    district = models.CharField('区县', max_length=50)
    street = models.CharField('街道', max_length=200)
    detail_address = models.TextField('详细地址')
    
    # 地理坐标
    longitude = models.DecimalField('经度', max_digits=10, decimal_places=7, blank=True, null=True)
    latitude = models.DecimalField('纬度', max_digits=10, decimal_places=7, blank=True, null=True)
    
    # 状态
    is_default = models.BooleanField('是否默认地址', default=False)
    
    class Meta:
        db_table = 'addresses_address'
        verbose_name = '用户地址'
        verbose_name_plural = '用户地址'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['longitude', 'latitude']),
        ]
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.province}{self.city}{self.district}{self.street}{self.detail_address}"
    
    def save(self, *args, **kwargs):
        # 如果设置为默认地址，取消其他默认地址
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)
