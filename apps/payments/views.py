from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Payment, Refund, UserBalance, BalanceTransaction
from .serializers import (
    PaymentSerializer, PaymentCreateSerializer, RefundSerializer,
    RefundCreateSerializer, UserBalanceSerializer, BalanceTransactionSerializer,
    BalanceRechargeSerializer, WeChatPaySerializer
)


class PaymentListView(generics.ListAPIView):
    """支付记录列表"""
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).order_by('-created_at')


class PaymentCreateView(generics.CreateAPIView):
    """支付创建"""
    serializer_class = PaymentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()
        
        return Response({
            'code': 200,
            'message': '支付创建成功',
            'data': PaymentSerializer(payment).data
        }, status=status.HTTP_201_CREATED)


class PaymentDetailView(generics.RetrieveAPIView):
    """支付详情"""
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)


class RefundListView(generics.ListAPIView):
    """退款记录列表"""
    serializer_class = RefundSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Refund.objects.filter(user=self.request.user).order_by('-created_at')


class RefundCreateView(generics.CreateAPIView):
    """退款申请"""
    serializer_class = RefundCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refund = serializer.save()
        
        return Response({
            'code': 200,
            'message': '退款申请提交成功',
            'data': RefundSerializer(refund).data
        }, status=status.HTTP_201_CREATED)


class UserBalanceView(generics.RetrieveAPIView):
    """用户余额"""
    serializer_class = UserBalanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        balance, created = UserBalance.objects.get_or_create(user=self.request.user)
        return balance


class BalanceTransactionListView(generics.ListAPIView):
    """余额交易记录"""
    serializer_class = BalanceTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return BalanceTransaction.objects.filter(user=self.request.user).order_by('-created_at')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_wechat_pay(request):
    """创建微信支付"""
    serializer = WeChatPaySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    payment_id = serializer.validated_data['payment_id']
    payment = Payment.objects.get(id=payment_id)
    
    # 这里应该调用微信支付API创建支付订单
    # 为了演示，我们返回模拟数据
    
    pay_data = {
        'appId': 'wx1234567890abcdef',
        'timeStamp': str(int(timezone.now().timestamp())),
        'nonceStr': 'random_string',
        'package': f'prepay_id=mock_prepay_id_{payment_id}',
        'signType': 'MD5',
        'paySign': 'mock_pay_sign'
    }
    
    return Response({
        'code': 200,
        'message': '微信支付创建成功',
        'data': {
            'payment_id': payment_id,
            'pay_data': pay_data
        }
    })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def wechat_pay_callback(request):
    """微信支付回调"""
    # 这里应该验证微信支付回调的签名
    # 为了演示，我们模拟处理支付成功
    
    payment_no = request.data.get('out_trade_no')
    transaction_id = request.data.get('transaction_id')
    
    try:
        payment = Payment.objects.get(payment_no=payment_no)
    except Payment.DoesNotExist:
        return Response({'code': 'FAIL', 'message': '支付记录不存在'})
    
    if payment.status == 'paid':
        return Response({'code': 'SUCCESS', 'message': 'OK'})
    
    # 更新支付状态
    payment.status = 'paid'
    payment.paid_at = timezone.now()
    payment.third_party_trade_no = transaction_id
    payment.save()
    
    # 更新订单状态
    order = payment.order
    order.payment_status = 'paid'
    order.payment_time = timezone.now()
    order.status = 'paid'
    order.save()
    
    # 记录订单状态变更日志
    from apps.orders.models import OrderStatusLog
    OrderStatusLog.objects.create(
        order=order,
        from_status='pending',
        to_status='paid',
        remark="支付成功"
    )
    
    return Response({'code': 'SUCCESS', 'message': 'OK'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def payment_status(request, payment_id):
    """查询支付状态"""
    try:
        payment = Payment.objects.get(id=payment_id, user=request.user)
    except Payment.DoesNotExist:
        return Response({
            'code': 404,
            'message': '支付记录不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    
    return Response({
        'code': 200,
        'message': 'success',
        'data': {
            'payment_id': payment.id,
            'status': payment.status,
            'status_display': payment.get_status_display(),
            'paid_at': payment.paid_at.isoformat() if payment.paid_at else None
        }
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def recharge_balance(request):
    """余额充值"""
    serializer = BalanceRechargeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    amount = serializer.validated_data['amount']
    payment_method = serializer.validated_data['payment_method']
    
    # 创建充值订单
    from apps.orders.models import Order
    order = Order.objects.create(
        user=request.user,
        order_no=f"RECHARGE{timezone.now().strftime('%Y%m%d%H%M%S')}",
        total_amount=amount,
        final_amount=amount,
        payment_method=payment_method,
        status='paid'
    )
    
    # 创建支付记录
    payment = Payment.objects.create(
        payment_no=f"PAY{timezone.now().strftime('%Y%m%d%H%M%S')}",
        order=order,
        user=request.user,
        payment_type=payment_method,
        amount=amount,
        status='paid',
        paid_at=timezone.now()
    )
    
    # 更新用户余额
    balance, created = UserBalance.objects.get_or_create(user=request.user)
    old_amount = balance.amount
    balance.amount += amount
    balance.save()
    
    # 记录余额交易
    BalanceTransaction.objects.create(
        transaction_no=f"TXN{timezone.now().strftime('%Y%m%d%H%M%S')}",
        user=request.user,
        transaction_type='recharge',
        amount=amount,
        balance_before=old_amount,
        balance_after=balance.amount,
        related_order=order,
        related_payment=payment,
        remark=f"余额充值 {amount}元"
    )
    
    return Response({
        'code': 200,
        'message': '充值成功',
        'data': {
            'amount': amount,
            'balance': float(balance.amount)
        }
    })
