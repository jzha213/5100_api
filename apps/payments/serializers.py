from rest_framework import serializers
from .models import Payment, Refund, UserBalance, BalanceTransaction


class PaymentSerializer(serializers.ModelSerializer):
    """支付记录序列化器"""
    order_no = serializers.CharField(source='order.order_no', read_only=True)
    payment_type_display = serializers.CharField(source='get_payment_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'payment_no', 'order_no', 'payment_type', 'payment_type_display',
            'amount', 'status', 'status_display', 'third_party_trade_no',
            'paid_at', 'expired_at', 'created_at'
        ]


class PaymentCreateSerializer(serializers.ModelSerializer):
    """支付创建序列化器"""
    order_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Payment
        fields = ['order_id', 'payment_type']
    
    def validate_order_id(self, value):
        """验证订单ID"""
        user = self.context['request'].user
        try:
            order = user.orders.get(id=value)
        except:
            raise serializers.ValidationError("订单不存在")
        
        if order.payment_status != 'unpaid':
            raise serializers.ValidationError("订单已支付或状态不正确")
        
        return value
    
    def create(self, validated_data):
        from apps.orders.models import Order
        from django.utils import timezone
        from datetime import timedelta
        
        order_id = validated_data.pop('order_id')
        order = Order.objects.get(id=order_id)
        user = self.context['request'].user
        
        # 生成支付单号
        payment_no = f"PAY{timezone.now().strftime('%Y%m%d%H%M%S')}{str(order.id).zfill(6)}"
        
        # 设置过期时间（30分钟）
        expired_at = timezone.now() + timedelta(minutes=30)
        
        payment = Payment.objects.create(
            payment_no=payment_no,
            order=order,
            user=user,
            amount=order.final_amount,
            expired_at=expired_at,
            **validated_data
        )
        
        return payment


class RefundSerializer(serializers.ModelSerializer):
    """退款记录序列化器"""
    order_no = serializers.CharField(source='order.order_no', read_only=True)
    payment_no = serializers.CharField(source='payment.payment_no', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    reviewer_name = serializers.CharField(source='reviewer.nickname', read_only=True)
    
    class Meta:
        model = Refund
        fields = [
            'id', 'refund_no', 'order_no', 'payment_no', 'amount', 'reason',
            'status', 'status_display', 'third_party_refund_no', 'refunded_at',
            'reviewer_name', 'review_remark', 'reviewed_at', 'created_at'
        ]


class RefundCreateSerializer(serializers.ModelSerializer):
    """退款创建序列化器"""
    order_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Refund
        fields = ['order_id', 'amount', 'reason']
    
    def validate_order_id(self, value):
        """验证订单ID"""
        user = self.context['request'].user
        try:
            order = user.orders.get(id=value)
        except:
            raise serializers.ValidationError("订单不存在")
        
        if order.payment_status != 'paid':
            raise serializers.ValidationError("订单未支付，无法退款")
        
        if order.status in ['cancelled', 'refunded']:
            raise serializers.ValidationError("订单已取消或已退款")
        
        return value
    
    def validate_amount(self, value):
        """验证退款金额"""
        if value <= 0:
            raise serializers.ValidationError("退款金额必须大于0")
        return value
    
    def create(self, validated_data):
        from apps.orders.models import Order
        from django.utils import timezone
        
        order_id = validated_data.pop('order_id')
        order = Order.objects.get(id=order_id)
        user = self.context['request'].user
        
        # 检查退款金额不能超过支付金额
        if validated_data['amount'] > order.final_amount:
            raise serializers.ValidationError("退款金额不能超过支付金额")
        
        # 生成退款单号
        refund_no = f"REF{timezone.now().strftime('%Y%m%d%H%M%S')}{str(order.id).zfill(6)}"
        
        refund = Refund.objects.create(
            refund_no=refund_no,
            payment=order.payment,
            order=order,
            user=user,
            **validated_data
        )
        
        return refund


class UserBalanceSerializer(serializers.ModelSerializer):
    """用户余额序列化器"""
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    available_amount = serializers.SerializerMethodField()
    
    class Meta:
        model = UserBalance
        fields = ['user_nickname', 'amount', 'frozen_amount', 'available_amount']
    
    def get_available_amount(self, obj):
        """可用余额"""
        return obj.amount - obj.frozen_amount


class BalanceTransactionSerializer(serializers.ModelSerializer):
    """余额交易记录序列化器"""
    transaction_type_display = serializers.CharField(source='get_transaction_type_display', read_only=True)
    related_order_no = serializers.CharField(source='related_order.order_no', read_only=True)
    
    class Meta:
        model = BalanceTransaction
        fields = [
            'id', 'transaction_no', 'transaction_type', 'transaction_type_display',
            'amount', 'balance_before', 'balance_after', 'related_order_no',
            'remark', 'created_at'
        ]


class BalanceRechargeSerializer(serializers.Serializer):
    """余额充值序列化器"""
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_method = serializers.ChoiceField(choices=['wechat', 'alipay'])
    
    def validate_amount(self, value):
        """验证充值金额"""
        if value <= 0:
            raise serializers.ValidationError("充值金额必须大于0")
        
        if value < 1:
            raise serializers.ValidationError("充值金额不能少于1元")
        
        if value > 10000:
            raise serializers.ValidationError("单次充值金额不能超过10000元")
        
        return value


class WeChatPaySerializer(serializers.Serializer):
    """微信支付序列化器"""
    payment_id = serializers.IntegerField()
    
    def validate_payment_id(self, value):
        """验证支付ID"""
        user = self.context['request'].user
        try:
            payment = user.payments.get(id=value)
        except:
            raise serializers.ValidationError("支付记录不存在")
        
        if payment.status != 'pending':
            raise serializers.ValidationError("支付状态不正确")
        
        return value
