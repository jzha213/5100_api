from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # 订单相关
    path('', views.OrderListView.as_view(), name='order-list'),
    path('create/', views.OrderCreateView.as_view(), name='order-create'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('<int:pk>/update/', views.OrderUpdateView.as_view(), name='order-update'),
    path('<int:pk>/delete/', views.OrderDestroyView.as_view(), name='order-delete'),
    path('<int:order_id>/cancel/', views.cancel_order, name='cancel-order'),
    path('<int:order_id>/confirm/', views.confirm_order, name='confirm-order'),
    
    # 购物车相关
    path('cart/', views.CartListView.as_view(), name='cart-list'),
    path('cart/create/', views.CartCreateView.as_view(), name='cart-create'),
    path('cart/<int:pk>/update/', views.CartUpdateView.as_view(), name='cart-update'),
    path('cart/<int:pk>/delete/', views.CartDestroyView.as_view(), name='cart-delete'),
    path('cart/summary/', views.cart_summary, name='cart-summary'),
    path('cart/clear/', views.clear_cart, name='clear-cart'),
]
