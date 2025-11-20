from rest_framework import serializers
from .models import DailyStatistics, UserBehavior, ProductAnalytics, SalesReport


class DailyStatisticsSerializer(serializers.ModelSerializer):
    """每日统计序列化器"""
    
    class Meta:
        model = DailyStatistics
        fields = [
            'id', 'date', 'new_users', 'active_users', 'total_users',
            'new_orders', 'paid_orders', 'completed_orders', 'cancelled_orders',
            'order_amount', 'paid_amount', 'refund_amount', 'product_views',
            'product_sales', 'created_at'
        ]


class UserBehaviorSerializer(serializers.ModelSerializer):
    """用户行为序列化器"""
    behavior_type_display = serializers.CharField(source='get_behavior_type_display', read_only=True)
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    order_no = serializers.CharField(source='order.order_no', read_only=True)
    
    class Meta:
        model = UserBehavior
        fields = [
            'id', 'user_nickname', 'behavior_type', 'behavior_type_display',
            'page_url', 'page_title', 'product_name', 'order_no', 'extra_data',
            'created_at'
        ]


class UserBehaviorCreateSerializer(serializers.ModelSerializer):
    """用户行为创建序列化器"""
    
    class Meta:
        model = UserBehavior
        fields = [
            'behavior_type', 'page_url', 'page_title', 'product', 'order', 'extra_data'
        ]
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ProductAnalyticsSerializer(serializers.ModelSerializer):
    """商品分析序列化器"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    
    class Meta:
        model = ProductAnalytics
        fields = [
            'id', 'product_name', 'product_sku', 'total_views', 'unique_views',
            'add_to_cart_count', 'order_count', 'conversion_rate', 'review_count',
            'average_rating', 'last_viewed_at', 'created_at'
        ]


class SalesReportSerializer(serializers.ModelSerializer):
    """销售报表序列化器"""
    report_type_display = serializers.CharField(source='get_report_type_display', read_only=True)
    
    class Meta:
        model = SalesReport
        fields = [
            'id', 'report_type', 'report_type_display', 'report_date',
            'total_orders', 'total_amount', 'total_profit', 'new_customers',
            'repeat_customers', 'top_products', 'top_categories',
            'average_order_value', 'order_cancellation_rate', 'created_at'
        ]


class StatisticsQuerySerializer(serializers.Serializer):
    """统计查询序列化器"""
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    report_type = serializers.ChoiceField(
        choices=['daily', 'weekly', 'monthly'],
        default='daily'
    )
    
    def validate(self, attrs):
        """验证日期范围"""
        start_date = attrs['start_date']
        end_date = attrs['end_date']
        
        if start_date > end_date:
            raise serializers.ValidationError("开始日期不能晚于结束日期")
        
        # 限制查询范围不超过一年
        from datetime import timedelta
        if (end_date - start_date).days > 365:
            raise serializers.ValidationError("查询范围不能超过一年")
        
        return attrs


class ProductStatisticsSerializer(serializers.Serializer):
    """商品统计序列化器"""
    product_id = serializers.IntegerField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    
    def validate_product_id(self, value):
        """验证商品ID"""
        from apps.products.models import Product
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("商品不存在")
        return value


class UserStatisticsSerializer(serializers.Serializer):
    """用户统计序列化器"""
    user_id = serializers.IntegerField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    
    def validate_user_id(self, value):
        """验证用户ID"""
        from apps.users.models import User
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("用户不存在")
        return value


class DashboardDataSerializer(serializers.Serializer):
    """仪表板数据序列化器"""
    # 今日数据
    today_orders = serializers.IntegerField()
    today_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    today_users = serializers.IntegerField()
    
    # 昨日数据
    yesterday_orders = serializers.IntegerField()
    yesterday_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    yesterday_users = serializers.IntegerField()
    
    # 本周数据
    week_orders = serializers.IntegerField()
    week_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    week_users = serializers.IntegerField()
    
    # 本月数据
    month_orders = serializers.IntegerField()
    month_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    month_users = serializers.IntegerField()
    
    # 增长率
    orders_growth_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    amount_growth_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    users_growth_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    
    # 热门商品
    top_products = serializers.ListField()
    
    # 订单状态分布
    order_status_distribution = serializers.DictField()
    
    # 最近7天趋势
    recent_7_days_trend = serializers.ListField()
