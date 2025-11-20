from django.db import models
from apps.common.models import BaseModel


class Notification(BaseModel):
    """通知模型"""
    NOTIFICATION_TYPE_CHOICES = [
        ('system', '系统通知'),
        ('order', '订单通知'),
        ('payment', '支付通知'),
        ('delivery', '配送通知'),
        ('promotion', '促销通知'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', '低'),
        ('normal', '普通'),
        ('high', '高'),
        ('urgent', '紧急'),
    ]
    
    # 基本信息
    title = models.CharField('通知标题', max_length=200)
    content = models.TextField('通知内容')
    notification_type = models.CharField('通知类型', max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    priority = models.CharField('优先级', max_length=20, choices=PRIORITY_CHOICES, default='normal')
    
    # 接收者
    target_users = models.ManyToManyField('users.User', blank=True, related_name='notifications')
    
    # 关联信息
    related_order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, blank=True, null=True, related_name='notifications')
    related_url = models.URLField('相关链接', blank=True)
    
    # 状态
    is_sent = models.BooleanField('是否已发送', default=False)
    sent_at = models.DateTimeField('发送时间', blank=True, null=True)
    
    # 时间设置
    scheduled_at = models.DateTimeField('计划发送时间', blank=True, null=True)
    expires_at = models.DateTimeField('过期时间', blank=True, null=True)
    
    class Meta:
        db_table = 'notifications_notification'
        verbose_name = '通知'
        verbose_name_plural = '通知'
        indexes = [
            models.Index(fields=['notification_type']),
            models.Index(fields=['priority']),
            models.Index(fields=['is_sent']),
            models.Index(fields=['scheduled_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class NotificationTemplate(BaseModel):
    """通知模板模型"""
    TEMPLATE_TYPE_CHOICES = [
        ('sms', '短信模板'),
        ('wechat', '微信模板'),
        ('email', '邮件模板'),
        ('push', '推送模板'),
    ]
    
    # 基本信息
    name = models.CharField('模板名称', max_length=100)
    template_type = models.CharField('模板类型', max_length=20, choices=TEMPLATE_TYPE_CHOICES)
    title_template = models.CharField('标题模板', max_length=200)
    content_template = models.TextField('内容模板')
    
    # 变量说明
    variables = models.JSONField('变量说明', default=dict, blank=True)
    
    # 状态
    is_active = models.BooleanField('是否启用', default=True)
    
    class Meta:
        db_table = 'notifications_notificationtemplate'
        verbose_name = '通知模板'
        verbose_name_plural = '通知模板'
        indexes = [
            models.Index(fields=['template_type']),
            models.Index(fields=['is_active']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.template_type}"


class NotificationLog(BaseModel):
    """通知发送日志模型"""
    STATUS_CHOICES = [
        ('pending', '待发送'),
        ('sent', '已发送'),
        ('failed', '发送失败'),
        ('delivered', '已送达'),
    ]
    
    # 基本信息
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='logs')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='notification_logs')
    
    # 发送信息
    channel = models.CharField('发送渠道', max_length=20)
    status = models.CharField('发送状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # 第三方信息
    third_party_id = models.CharField('第三方ID', max_length=100, blank=True)
    third_party_response = models.JSONField('第三方响应', default=dict, blank=True)
    
    # 时间信息
    sent_at = models.DateTimeField('发送时间', blank=True, null=True)
    delivered_at = models.DateTimeField('送达时间', blank=True, null=True)
    
    # 错误信息
    error_message = models.TextField('错误信息', blank=True)
    
    class Meta:
        db_table = 'notifications_notificationlog'
        verbose_name = '通知发送日志'
        verbose_name_plural = '通知发送日志'
        indexes = [
            models.Index(fields=['notification']),
            models.Index(fields=['user']),
            models.Index(fields=['status']),
            models.Index(fields=['channel']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.notification.title} - {self.user.nickname} - {self.status}"


class Message(BaseModel):
    """消息模型"""
    MESSAGE_TYPE_CHOICES = [
        ('system', '系统消息'),
        ('order', '订单消息'),
        ('customer_service', '客服消息'),
        ('marketing', '营销消息'),
    ]
    
    # 基本信息
    title = models.CharField('消息标题', max_length=200)
    content = models.TextField('消息内容')
    message_type = models.CharField('消息类型', max_length=20, choices=MESSAGE_TYPE_CHOICES)
    
    # 接收者
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='messages')
    
    # 状态
    is_read = models.BooleanField('是否已读', default=False)
    read_at = models.DateTimeField('阅读时间', blank=True, null=True)
    
    # 关联信息
    related_order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, blank=True, null=True, related_name='messages')
    
    class Meta:
        db_table = 'notifications_message'
        verbose_name = '消息'
        verbose_name_plural = '消息'
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['message_type']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.nickname}"
