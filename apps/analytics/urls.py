from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    # 统计数据
    path('daily/', views.DailyStatisticsListView.as_view(), name='daily-statistics-list'),
    path('dashboard/', views.dashboard_data, name='dashboard-data'),
    path('report/generate/', views.generate_sales_report, name='generate-sales-report'),
    
    # 用户行为
    path('behaviors/', views.UserBehaviorListView.as_view(), name='user-behavior-list'),
    path('behaviors/create/', views.UserBehaviorCreateView.as_view(), name='user-behavior-create'),
    path('behaviors/record/', views.record_user_behavior, name='record-user-behavior'),
    
    # 商品分析
    path('products/', views.ProductAnalyticsListView.as_view(), name='product-analytics-list'),
    path('products/<int:product_id>/statistics/', views.product_statistics, name='product-statistics'),
    
    # 销售报表
    path('reports/', views.SalesReportListView.as_view(), name='sales-report-list'),
]
