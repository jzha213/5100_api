from django.urls import path
from . import views

app_name = 'coupons'

urlpatterns = [
    # 优惠券相关
    path('', views.CouponListView.as_view(), name='coupon-list'),
    path('create/', views.CouponCreateView.as_view(), name='coupon-create'),
    path('validate/', views.validate_coupon, name='validate-coupon'),
    path('available/', views.available_coupons, name='available-coupons'),
    path('stats/', views.coupon_stats, name='coupon-stats'),
    path('use/', views.use_coupon, name='use-coupon'),
    
    # 用户优惠券相关
    path('user/', views.UserCouponListView.as_view(), name='user-coupon-list'),
    path('user/create/', views.UserCouponCreateView.as_view(), name='user-coupon-create'),
    
    # 优惠券使用记录
    path('usage/', views.CouponUsageListView.as_view(), name='coupon-usage-list'),
]
