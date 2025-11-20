from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # 支付相关
    path('', views.PaymentListView.as_view(), name='payment-list'),
    path('create/', views.PaymentCreateView.as_view(), name='payment-create'),
    path('<int:pk>/', views.PaymentDetailView.as_view(), name='payment-detail'),
    path('wechat/create/', views.create_wechat_pay, name='wechat-pay-create'),
    path('wechat/callback/', views.wechat_pay_callback, name='wechat-pay-callback'),
    path('<int:payment_id>/status/', views.payment_status, name='payment-status'),
    
    # 退款相关
    path('refunds/', views.RefundListView.as_view(), name='refund-list'),
    path('refunds/create/', views.RefundCreateView.as_view(), name='refund-create'),
    
    # 余额相关
    path('balance/', views.UserBalanceView.as_view(), name='user-balance'),
    path('balance/transactions/', views.BalanceTransactionListView.as_view(), name='balance-transactions'),
    path('balance/recharge/', views.recharge_balance, name='balance-recharge'),
]
