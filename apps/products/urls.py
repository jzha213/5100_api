from django.urls import path
from . import views_simple

app_name = 'products'

urlpatterns = [
    # 简化的API路由
    path('', views_simple.product_list, name='product-list'),
    path('categories/', views_simple.category_list, name='category-list'),
    path('<int:pk>/', views_simple.product_detail, name='product-detail'),
]
