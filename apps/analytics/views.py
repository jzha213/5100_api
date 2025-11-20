from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Sum, Count, Avg
from datetime import datetime, timedelta
from .models import DailyStatistics, UserBehavior, ProductAnalytics, SalesReport
from .serializers import (
    DailyStatisticsSerializer, UserBehaviorSerializer, UserBehaviorCreateSerializer,
    ProductAnalyticsSerializer, SalesReportSerializer, StatisticsQuerySerializer,
    ProductStatisticsSerializer, UserStatisticsSerializer, DashboardDataSerializer
)


class DailyStatisticsListView(generics.ListAPIView):
    """每日统计列表"""
    serializer_class = DailyStatisticsSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        return DailyStatistics.objects.all().order_by('-date')


class UserBehaviorListView(generics.ListAPIView):
    """用户行为列表"""
    serializer_class = UserBehaviorSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        return UserBehavior.objects.all().order_by('-created_at')


class UserBehaviorCreateView(generics.CreateAPIView):
    """用户行为记录"""
    serializer_class = UserBehaviorCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductAnalyticsListView(generics.ListAPIView):
    """商品分析列表"""
    serializer_class = ProductAnalyticsSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        return ProductAnalytics.objects.all().order_by('-total_views')


class SalesReportListView(generics.ListAPIView):
    """销售报表列表"""
    serializer_class = SalesReportSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        return SalesReport.objects.all().order_by('-report_date')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def record_user_behavior(request):
    """记录用户行为"""
    serializer = UserBehaviorCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    behavior = serializer.save()
    
    return Response({
        'code': 200,
        'message': '行为记录成功',
        'data': UserBehaviorSerializer(behavior).data
    })


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def dashboard_data(request):
    """仪表板数据"""
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    week_start = today - timedelta(days=7)
    month_start = today.replace(day=1)
    
    # 今日数据
    from apps.orders.models import Order
    from apps.users.models import User
    
    today_orders = Order.objects.filter(created_at__date=today).count()
    today_amount = Order.objects.filter(created_at__date=today, payment_status='paid').aggregate(
        total=Sum('final_amount'))['total'] or 0
    today_users = User.objects.filter(created_at__date=today).count()
    
    # 昨日数据
    yesterday_orders = Order.objects.filter(created_at__date=yesterday).count()
    yesterday_amount = Order.objects.filter(created_at__date=yesterday, payment_status='paid').aggregate(
        total=Sum('final_amount'))['total'] or 0
    yesterday_users = User.objects.filter(created_at__date=yesterday).count()
    
    # 本周数据
    week_orders = Order.objects.filter(created_at__date__gte=week_start).count()
    week_amount = Order.objects.filter(created_at__date__gte=week_start, payment_status='paid').aggregate(
        total=Sum('final_amount'))['total'] or 0
    week_users = User.objects.filter(created_at__date__gte=week_start).count()
    
    # 本月数据
    month_orders = Order.objects.filter(created_at__date__gte=month_start).count()
    month_amount = Order.objects.filter(created_at__date__gte=month_start, payment_status='paid').aggregate(
        total=Sum('final_amount'))['total'] or 0
    month_users = User.objects.filter(created_at__date__gte=month_start).count()
    
    # 计算增长率
    orders_growth_rate = ((today_orders - yesterday_orders) / yesterday_orders * 100) if yesterday_orders > 0 else 0
    amount_growth_rate = ((today_amount - yesterday_amount) / yesterday_amount * 100) if yesterday_amount > 0 else 0
    users_growth_rate = ((today_users - yesterday_users) / yesterday_users * 100) if yesterday_users > 0 else 0
    
    # 热门商品
    from apps.products.models import Product
    top_products = Product.objects.filter(is_active=True).order_by('-sales_count')[:5].values(
        'id', 'name', 'sales_count', 'price'
    )
    
    # 订单状态分布
    order_status_distribution = {}
    for status, _ in Order.STATUS_CHOICES:
        count = Order.objects.filter(status=status).count()
        order_status_distribution[status] = count
    
    # 最近7天趋势
    recent_7_days_trend = []
    for i in range(7):
        date = today - timedelta(days=i)
        orders_count = Order.objects.filter(created_at__date=date).count()
        amount = Order.objects.filter(created_at__date=date, payment_status='paid').aggregate(
            total=Sum('final_amount'))['total'] or 0
        
        recent_7_days_trend.append({
            'date': date.isoformat(),
            'orders': orders_count,
            'amount': float(amount)
        })
    
    recent_7_days_trend.reverse()
    
    data = {
        'today_orders': today_orders,
        'today_amount': float(today_amount),
        'today_users': today_users,
        'yesterday_orders': yesterday_orders,
        'yesterday_amount': float(yesterday_amount),
        'yesterday_users': yesterday_users,
        'week_orders': week_orders,
        'week_amount': float(week_amount),
        'week_users': week_users,
        'month_orders': month_orders,
        'month_amount': float(month_amount),
        'month_users': month_users,
        'orders_growth_rate': round(orders_growth_rate, 2),
        'amount_growth_rate': round(amount_growth_rate, 2),
        'users_growth_rate': round(users_growth_rate, 2),
        'top_products': list(top_products),
        'order_status_distribution': order_status_distribution,
        'recent_7_days_trend': recent_7_days_trend
    }
    
    return Response({
        'code': 200,
        'message': 'success',
        'data': data
    })


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def generate_sales_report(request):
    """生成销售报表"""
    serializer = StatisticsQuerySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    start_date = serializer.validated_data['start_date']
    end_date = serializer.validated_data['end_date']
    report_type = serializer.validated_data['report_type']
    
    from apps.orders.models import Order
    from apps.users.models import User
    
    # 根据报表类型生成数据
    if report_type == 'daily':
        report_date = end_date
    elif report_type == 'weekly':
        # 获取周的开始日期
        report_date = start_date
    elif report_type == 'monthly':
        report_date = start_date.replace(day=1)
    else:
        report_date = start_date.replace(month=1, day=1)
    
    # 查询数据
    orders = Order.objects.filter(created_at__date__range=[start_date, end_date])
    
    total_orders = orders.count()
    total_amount = orders.filter(payment_status='paid').aggregate(
        total=Sum('final_amount'))['total'] or 0
    total_profit = total_amount * 0.2  # 假设利润率20%
    
    new_customers = User.objects.filter(
        created_at__date__range=[start_date, end_date]
    ).count()
    
    repeat_customers = User.objects.filter(
        orders__created_at__date__range=[start_date, end_date]
    ).distinct().count() - new_customers
    
    # 热门商品
    from apps.products.models import Product
    top_products = Product.objects.filter(
        orderitem__order__created_at__date__range=[start_date, end_date]
    ).annotate(
        total_sales=Sum('orderitem__quantity')
    ).order_by('-total_sales')[:10].values('id', 'name', 'total_sales')
    
    # 热门分类
    from apps.products.models import Category
    top_categories = Category.objects.filter(
        products__orderitem__order__created_at__date__range=[start_date, end_date]
    ).annotate(
        total_sales=Sum('products__orderitem__quantity')
    ).order_by('-total_sales')[:5].values('id', 'name', 'total_sales')
    
    average_order_value = total_amount / total_orders if total_orders > 0 else 0
    order_cancellation_rate = orders.filter(status='cancelled').count() / total_orders * 100 if total_orders > 0 else 0
    
    # 创建或更新销售报表
    report, created = SalesReport.objects.get_or_create(
        report_type=report_type,
        report_date=report_date,
        defaults={
            'total_orders': total_orders,
            'total_amount': total_amount,
            'total_profit': total_profit,
            'new_customers': new_customers,
            'repeat_customers': repeat_customers,
            'top_products': list(top_products),
            'top_categories': list(top_categories),
            'average_order_value': average_order_value,
            'order_cancellation_rate': order_cancellation_rate
        }
    )
    
    if not created:
        report.total_orders = total_orders
        report.total_amount = total_amount
        report.total_profit = total_profit
        report.new_customers = new_customers
        report.repeat_customers = repeat_customers
        report.top_products = list(top_products)
        report.top_categories = list(top_categories)
        report.average_order_value = average_order_value
        report.order_cancellation_rate = order_cancellation_rate
        report.save()
    
    return Response({
        'code': 200,
        'message': '销售报表生成成功',
        'data': SalesReportSerializer(report).data
    })


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def product_statistics(request, product_id):
    """商品统计"""
    try:
        from apps.products.models import Product
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({
            'code': 404,
            'message': '商品不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # 查询指定时间范围的数据
        behaviors = UserBehavior.objects.filter(
            product=product,
            created_at__date__range=[start_date, end_date]
        )
        
        views = behaviors.filter(behavior_type='product_view').count()
        add_to_cart = behaviors.filter(behavior_type='add_to_cart').count()
        
        from apps.orders.models import OrderItem
        orders = OrderItem.objects.filter(
            product=product,
            order__created_at__date__range=[start_date, end_date]
        ).aggregate(
            total_quantity=Sum('quantity'),
            total_amount=Sum('subtotal')
        )
    else:
        # 查询所有数据
        views = product.analytics.total_views if hasattr(product, 'analytics') else 0
        add_to_cart = product.analytics.add_to_cart_count if hasattr(product, 'analytics') else 0
        
        from apps.orders.models import OrderItem
        orders = OrderItem.objects.filter(product=product).aggregate(
            total_quantity=Sum('quantity'),
            total_amount=Sum('subtotal')
        )
    
    conversion_rate = (orders['total_quantity'] / views * 100) if views > 0 else 0
    
    return Response({
        'code': 200,
        'message': 'success',
        'data': {
            'product_id': product.id,
            'product_name': product.name,
            'views': views,
            'add_to_cart': add_to_cart,
            'orders': orders['total_quantity'] or 0,
            'amount': float(orders['total_amount'] or 0),
            'conversion_rate': round(conversion_rate, 2)
        }
    })
