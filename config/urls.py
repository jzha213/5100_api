"""
URL configuration for 5100 water delivery project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.shortcuts import render

# Simple health check view
def health_check(request):
    return JsonResponse({'status': 'healthy', 'message': '5100 Water Delivery API is running'})

# Home page view
def home(request):
    """主页面视图"""
    return render(request, 'index.html')

urlpatterns = [
    # Home page - 主页面
    path('', home, name='home'),
    
    # Health check
    path('health/', health_check, name='health-check'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation (disabled for now)
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API v1 - 启用商品API和用户认证API
    path('api/v1/products/', include('apps.products.urls')),
    path('api/v1/auth/', include('apps.users.urls_simple')),
    # 开放基础业务接口，便于小程序联调
    path('api/v1/orders/', include('apps.orders.urls')),
    # path('api/v1/payments/', include('apps.payments.urls')),
    # path('api/v1/delivery/', include('apps.delivery.urls')),
    path('api/v1/addresses/', include('apps.addresses.urls')),
    # path('api/v1/coupons/', include('apps.coupons.urls')),
    # path('api/v1/notifications/', include('apps.notifications.urls')),
    # path('api/v1/analytics/', include('apps.analytics.urls')),
    # 购物车API通过orders应用提供
    path('api/v1/cart/', include('apps.orders.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # 添加assets路径的静态文件服务
    urlpatterns += static('/assets/', document_root=settings.BASE_DIR / 'static' / 'assets')
