from django.db import models
from apps.common.models import BaseModel


class DailyStatistics(BaseModel):
    """每日统计模型"""
    date = models.DateField('日期', unique=True)
    
    # 用户统计
    new_users = models.IntegerField('新增用户', default=0)
    active_users = models.IntegerField('活跃用户', default=0)
    total_users = models.IntegerField('总用户数', default=0)
    
    # 订单统计
    new_orders = models.IntegerField('新增订单', default=0)
    paid_orders = models.IntegerField('已支付订单', default=0)
    completed_orders = models.IntegerField('已完成订单', default=0)
    cancelled_orders = models.IntegerField('已取消订单', default=0)
    
    # 金额统计
    order_amount = models.DecimalField('订单金额', max_digits=12, decimal_places=2, default=0)
    paid_amount = models.DecimalField('支付金额', max_digits=12, decimal_places=2, default=0)
    refund_amount = models.DecimalField('退款金额', max_digits=12, decimal_places=2, default=0)
    
    # 商品统计
    product_views = models.IntegerField('商品浏览量', default=0)
    product_sales = models.IntegerField('商品销量', default=0)
    
    class Meta:
        db_table = 'analytics_dailystatistics'
        verbose_name = '每日统计'
        verbose_name_plural = '每日统计'
        indexes = [
            models.Index(fields=['date']),
        ]
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.date} - 统计"


class UserBehavior(BaseModel):
    """用户行为模型"""
    BEHAVIOR_TYPE_CHOICES = [
        ('page_view', '页面浏览'),
        ('product_view', '商品浏览'),
        ('add_to_cart', '加入购物车'),
        ('remove_from_cart', '移除购物车'),
        ('order_create', '创建订单'),
        ('order_pay', '支付订单'),
        ('order_cancel', '取消订单'),
        ('search', '搜索'),
        ('share', '分享'),
        ('collect', '收藏'),
    ]
    
    # 基本信息
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='behaviors')
    behavior_type = models.CharField('行为类型', max_length=20, choices=BEHAVIOR_TYPE_CHOICES)
    
    # 页面信息
    page_url = models.URLField('页面URL', blank=True)
    page_title = models.CharField('页面标题', max_length=200, blank=True)
    
    # 商品信息
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, blank=True, null=True, related_name='user_behaviors')
    
    # 订单信息
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, blank=True, null=True, related_name='user_behaviors')
    
    # 其他信息
    extra_data = models.JSONField('额外数据', default=dict, blank=True)
    
    class Meta:
        db_table = 'analytics_userbehavior'
        verbose_name = '用户行为'
        verbose_name_plural = '用户行为'
        indexes = [
            models.Index(fields=['user', 'behavior_type']),
            models.Index(fields=['behavior_type']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.nickname} - {self.behavior_type}"


class ProductAnalytics(BaseModel):
    """商品分析模型"""
    product = models.OneToOneField('products.Product', on_delete=models.CASCADE, related_name='analytics')
    
    # 浏览统计
    total_views = models.IntegerField('总浏览量', default=0)
    unique_views = models.IntegerField('独立访客数', default=0)
    
    # 转化统计
    add_to_cart_count = models.IntegerField('加入购物车次数', default=0)
    order_count = models.IntegerField('订单数量', default=0)
    conversion_rate = models.DecimalField('转化率', max_digits=5, decimal_places=2, default=0)
    
    # 评价统计
    review_count = models.IntegerField('评价数量', default=0)
    average_rating = models.DecimalField('平均评分', max_digits=3, decimal_places=2, default=0)
    
    # 时间统计
    last_viewed_at = models.DateTimeField('最后浏览时间', blank=True, null=True)
    
    class Meta:
        db_table = 'analytics_productanalytics'
        verbose_name = '商品分析'
        verbose_name_plural = '商品分析'
    
    def __str__(self):
        return f"{self.product.name} - 分析数据"


class SalesReport(BaseModel):
    """销售报表模型"""
    REPORT_TYPE_CHOICES = [
        ('daily', '日报'),
        ('weekly', '周报'),
        ('monthly', '月报'),
        ('yearly', '年报'),
    ]
    
    # 基本信息
    report_type = models.CharField('报表类型', max_length=20, choices=REPORT_TYPE_CHOICES)
    report_date = models.DateField('报表日期')
    
    # 销售统计
    total_orders = models.IntegerField('总订单数', default=0)
    total_amount = models.DecimalField('总销售额', max_digits=12, decimal_places=2, default=0)
    total_profit = models.DecimalField('总利润', max_digits=12, decimal_places=2, default=0)
    
    # 用户统计
    new_customers = models.IntegerField('新客户数', default=0)
    repeat_customers = models.IntegerField('回头客数', default=0)
    
    # 商品统计
    top_products = models.JSONField('热销商品', default=list, blank=True)
    top_categories = models.JSONField('热销分类', default=list, blank=True)
    
    # 其他统计
    average_order_value = models.DecimalField('平均订单价值', max_digits=10, decimal_places=2, default=0)
    order_cancellation_rate = models.DecimalField('订单取消率', max_digits=5, decimal_places=2, default=0)
    
    class Meta:
        db_table = 'analytics_salesreport'
        verbose_name = '销售报表'
        verbose_name_plural = '销售报表'
        unique_together = ['report_type', 'report_date']
        indexes = [
            models.Index(fields=['report_type', 'report_date']),
        ]
        ordering = ['-report_date']
    
    def __str__(self):
        return f"{self.report_type} - {self.report_date}"
