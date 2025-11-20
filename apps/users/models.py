from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.common.models import BaseModel


class User(AbstractUser):
    """用户模型"""
    GENDER_CHOICES = [
        (0, '未知'),
        (1, '男'),
        (2, '女'),
    ]
    
    STATUS_CHOICES = [
        (0, '禁用'),
        (1, '正常'),
    ]
    
    # 微信相关字段
    openid = models.CharField('微信OpenID', max_length=64, unique=True, blank=True, null=True)
    unionid = models.CharField('微信UnionID', max_length=64, unique=True, blank=True, null=True)
    
    # 基本信息
    nickname = models.CharField('昵称', max_length=100, blank=True)
    avatar_url = models.URLField('头像URL', blank=True)
    phone = models.CharField('手机号', max_length=20, unique=True, blank=True, null=True)
    gender = models.SmallIntegerField('性别', choices=GENDER_CHOICES, default=0)
    birthday = models.DateField('生日', blank=True, null=True)
    
    # VIP相关
    is_vip = models.BooleanField('是否VIP', default=False)
    vip_expire_at = models.DateTimeField('VIP过期时间', blank=True, null=True)
    
    # 积分和消费
    points = models.IntegerField('积分', default=0)
    total_consumption = models.DecimalField('总消费金额', max_digits=10, decimal_places=2, default=0)
    
    # 状态
    status = models.SmallIntegerField('状态', choices=STATUS_CHOICES, default=1)
    
    # 时间字段
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'users_user'
        verbose_name = '用户'
        verbose_name_plural = '用户'
        indexes = [
            models.Index(fields=['openid']),
            models.Index(fields=['phone']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return self.nickname or self.username


class UserProfile(BaseModel):
    """用户资料模型"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    real_name = models.CharField('真实姓名', max_length=50, blank=True)
    id_card = models.CharField('身份证号', max_length=18, blank=True)
    address = models.TextField('地址', blank=True)
    emergency_contact = models.CharField('紧急联系人', max_length=50, blank=True)
    emergency_phone = models.CharField('紧急联系电话', max_length=20, blank=True)
    
    class Meta:
        db_table = 'users_userprofile'
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'
    
    def __str__(self):
        return f"{self.user.nickname}的资料"


class UserLoginLog(BaseModel):
    """用户登录日志"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_logs')
    login_ip = models.GenericIPAddressField('登录IP')
    user_agent = models.TextField('用户代理', blank=True)
    login_type = models.CharField('登录类型', max_length=20, default='wechat')
    
    class Meta:
        db_table = 'users_userloginlog'
        verbose_name = '用户登录日志'
        verbose_name_plural = '用户登录日志'
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.nickname} - {self.login_ip} - {self.created_at}"
