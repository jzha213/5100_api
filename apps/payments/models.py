from django.db import models
from apps.common.models import BaseModel


class Payment(BaseModel):
    """支付记录模型"""
    PAYMENT_TYPE_CHOICES = [
        ('wechat', '微信支付'),
        ('alipay', '支付宝'),
        ('balance', '余额支付'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('failed', '支付失败'),
        ('cancelled', '已取消'),
        ('refunding', '退款中'),
        ('refunded', '已退款'),
        ('refund_failed', '退款失败'),
    ]
    
    # 基本信息
    payment_no = models.CharField('支付单号', max_length=32, unique=True)
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='payment')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='payments')
    
    # 支付信息
    payment_type = models.CharField('支付方式', max_length=20, choices=PAYMENT_TYPE_CHOICES)
    amount = models.DecimalField('支付金额', max_digits=10, decimal_places=2)
    status = models.CharField('支付状态', max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # 第三方支付信息
    third_party_trade_no = models.CharField('第三方交易号', max_length=100, blank=True)
    third_party_response = models.JSONField('第三方响应数据', default=dict, blank=True)
    
    # 时间信息
    paid_at = models.DateTimeField('支付时间', blank=True, null=True)
    expired_at = models.DateTimeField('过期时间', blank=True, null=True)
    
    # 其他信息
    remark = models.TextField('备注', blank=True)
    
    class Meta:
        db_table = 'payments_payment'
        verbose_name = '支付记录'
        verbose_name_plural = '支付记录'
        indexes = [
            models.Index(fields=['payment_no']),
            models.Index(fields=['order']),
            models.Index(fields=['user']),
            models.Index(fields=['status']),
            models.Index(fields=['third_party_trade_no']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"支付单{self.payment_no} - {self.amount}元"


class Refund(BaseModel):
    """退款记录模型"""
    REFUND_STATUS_CHOICES = [
        ('pending', '退款中'),
        ('success', '退款成功'),
        ('failed', '退款失败'),
        ('cancelled', '已取消'),
    ]
    
    # 基本信息
    refund_no = models.CharField('退款单号', max_length=32, unique=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='refunds')
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='refunds')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='refunds')
    
    # 退款信息
    amount = models.DecimalField('退款金额', max_digits=10, decimal_places=2)
    reason = models.TextField('退款原因')
    status = models.CharField('退款状态', max_length=20, choices=REFUND_STATUS_CHOICES, default='pending')
    
    # 第三方退款信息
    third_party_refund_no = models.CharField('第三方退款号', max_length=100, blank=True)
    third_party_response = models.JSONField('第三方响应数据', default=dict, blank=True)
    
    # 时间信息
    refunded_at = models.DateTimeField('退款时间', blank=True, null=True)
    
    # 审核信息
    reviewer = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=True, null=True, related_name='reviewed_refunds')
    review_remark = models.TextField('审核备注', blank=True)
    reviewed_at = models.DateTimeField('审核时间', blank=True, null=True)
    
    class Meta:
        db_table = 'payments_refund'
        verbose_name = '退款记录'
        verbose_name_plural = '退款记录'
        indexes = [
            models.Index(fields=['refund_no']),
            models.Index(fields=['payment']),
            models.Index(fields=['order']),
            models.Index(fields=['user']),
            models.Index(fields=['status']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"退款单{self.refund_no} - {self.amount}元"


class UserBalance(BaseModel):
    """用户余额模型"""
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='balance')
    amount = models.DecimalField('余额', max_digits=10, decimal_places=2, default=0)
    frozen_amount = models.DecimalField('冻结金额', max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        db_table = 'payments_userbalance'
        verbose_name = '用户余额'
        verbose_name_plural = '用户余额'
    
    def __str__(self):
        return f"{self.user.nickname} - {self.amount}元"


class BalanceTransaction(BaseModel):
    """余额交易记录模型"""
    TRANSACTION_TYPE_CHOICES = [
        ('recharge', '充值'),
        ('consume', '消费'),
        ('refund', '退款'),
        ('freeze', '冻结'),
        ('unfreeze', '解冻'),
    ]
    
    # 基本信息
    transaction_no = models.CharField('交易单号', max_length=32, unique=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='balance_transactions')
    
    # 交易信息
    transaction_type = models.CharField('交易类型', max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField('交易金额', max_digits=10, decimal_places=2)
    balance_before = models.DecimalField('交易前余额', max_digits=10, decimal_places=2)
    balance_after = models.DecimalField('交易后余额', max_digits=10, decimal_places=2)
    
    # 关联信息
    related_order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, blank=True, null=True)
    related_payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)
    
    # 其他信息
    remark = models.TextField('备注', blank=True)
    
    class Meta:
        db_table = 'payments_balancetransaction'
        verbose_name = '余额交易记录'
        verbose_name_plural = '余额交易记录'
        indexes = [
            models.Index(fields=['transaction_no']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['transaction_type']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.nickname} - {self.transaction_type} - {self.amount}元"
