from rest_framework import serializers
from .models import Coupon, UserCoupon, CouponUsage


class CouponSerializer(serializers.ModelSerializer):
    """优惠券序列化器"""
    coupon_type_display = serializers.CharField(source='get_coupon_type_display', read_only=True)
    is_valid = serializers.ReadOnlyField()
    
    class Meta:
        model = Coupon
        fields = [
            'id', 'name', 'description', 'coupon_type', 'coupon_type_display',
            'discount_value', 'discount_rate', 'min_amount', 'max_discount',
            'total_count', 'used_count', 'per_user_limit', 'valid_from',
            'valid_to', 'is_valid', 'is_active'
        ]


class CouponCreateSerializer(serializers.ModelSerializer):
    """优惠券创建序列化器"""
    
    class Meta:
        model = Coupon
        fields = [
            'name', 'description', 'coupon_type', 'discount_value', 'discount_rate',
            'min_amount', 'max_discount', 'total_count', 'per_user_limit',
            'valid_from', 'valid_to', 'applicable_products', 'applicable_categories',
            'is_active'
        ]
    
    def validate(self, attrs):
        """验证优惠券数据"""
        coupon_type = attrs.get('coupon_type')
        discount_value = attrs.get('discount_value', 0)
        discount_rate = attrs.get('discount_rate')
        min_amount = attrs.get('min_amount', 0)
        max_discount = attrs.get('max_discount')
        
        if coupon_type == 'discount':
            if not discount_rate:
                raise serializers.ValidationError("折扣券必须设置折扣率")
            if not (0 < discount_rate <= 100):
                raise serializers.ValidationError("折扣率必须在0-100之间")
        elif coupon_type == 'cash':
            if not discount_value or discount_value <= 0:
                raise serializers.ValidationError("现金券必须设置优惠金额")
        elif coupon_type == 'free_shipping':
            if discount_value != 0:
                raise serializers.ValidationError("免运费券优惠金额应为0")
        
        if min_amount < 0:
            raise serializers.ValidationError("最低消费金额不能为负数")
        
        if max_discount and max_discount <= 0:
            raise serializers.ValidationError("最大优惠金额必须大于0")
        
        return attrs


class UserCouponSerializer(serializers.ModelSerializer):
    """用户优惠券序列化器"""
    coupon_name = serializers.CharField(source='coupon.name', read_only=True)
    coupon_description = serializers.TextField(source='coupon.description', read_only=True)
    coupon_type = serializers.CharField(source='coupon.coupon_type', read_only=True)
    coupon_type_display = serializers.CharField(source='coupon.get_coupon_type_display', read_only=True)
    discount_value = serializers.DecimalField(source='coupon.discount_value', max_digits=10, decimal_places=2, read_only=True)
    discount_rate = serializers.DecimalField(source='coupon.discount_rate', max_digits=5, decimal_places=2, read_only=True)
    min_amount = serializers.DecimalField(source='coupon.min_amount', max_digits=10, decimal_places=2, read_only=True)
    max_discount = serializers.DecimalField(source='coupon.max_discount', max_digits=10, decimal_places=2, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_expired = serializers.ReadOnlyField()
    
    class Meta:
        model = UserCoupon
        fields = [
            'id', 'coupon_name', 'coupon_description', 'coupon_type', 'coupon_type_display',
            'discount_value', 'discount_rate', 'min_amount', 'max_discount',
            'status', 'status_display', 'used_at', 'expired_at', 'is_expired',
            'created_at'
        ]


class UserCouponCreateSerializer(serializers.Serializer):
    """用户优惠券领取序列化器"""
    coupon_id = serializers.IntegerField()
    
    def validate_coupon_id(self, value):
        """验证优惠券ID"""
        try:
            coupon = Coupon.objects.get(id=value)
        except Coupon.DoesNotExist:
            raise serializers.ValidationError("优惠券不存在")
        
        if not coupon.is_valid:
            raise serializers.ValidationError("优惠券已失效")
        
        return value
    
    def validate(self, attrs):
        """验证领取条件"""
        coupon_id = attrs['coupon_id']
        user = self.context['request'].user
        
        coupon = Coupon.objects.get(id=coupon_id)
        
        # 检查用户是否已达到领取上限
        user_coupon_count = UserCoupon.objects.filter(
            user=user,
            coupon=coupon
        ).count()
        
        if user_coupon_count >= coupon.per_user_limit:
            raise serializers.ValidationError(f"已达到领取上限，最多可领取{coupon.per_user_limit}张")
        
        return attrs
    
    def create(self, validated_data):
        coupon_id = validated_data['coupon_id']
        user = self.context['request'].user
        
        coupon = Coupon.objects.get(id=coupon_id)
        
        # 创建用户优惠券
        user_coupon = UserCoupon.objects.create(
            user=user,
            coupon=coupon,
            expired_at=coupon.valid_to
        )
        
        return user_coupon


class CouponUsageSerializer(serializers.ModelSerializer):
    """优惠券使用记录序列化器"""
    user_coupon_name = serializers.CharField(source='user_coupon.coupon.name', read_only=True)
    order_no = serializers.CharField(source='order.order_no', read_only=True)
    
    class Meta:
        model = CouponUsage
        fields = [
            'id', 'user_coupon_name', 'order_no', 'discount_amount', 'created_at'
        ]


class CouponValidateSerializer(serializers.Serializer):
    """优惠券验证序列化器"""
    coupon_code = serializers.CharField(max_length=100)
    order_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    def validate_coupon_code(self, value):
        """验证优惠券代码"""
        if not value:
            raise serializers.ValidationError("优惠券代码不能为空")
        return value
    
    def validate_order_amount(self, value):
        """验证订单金额"""
        if value <= 0:
            raise serializers.ValidationError("订单金额必须大于0")
        return value
    
    def validate(self, attrs):
        """验证优惠券使用条件"""
        coupon_code = attrs['coupon_code']
        order_amount = attrs['order_amount']
        user = self.context['request'].user
        
        try:
            user_coupon = UserCoupon.objects.get(
                user=user,
                coupon__name=coupon_code  # 这里假设优惠券代码就是优惠券名称
            )
        except UserCoupon.DoesNotExist:
            raise serializers.ValidationError("优惠券不存在或未领取")
        
        if user_coupon.status != 'unused':
            raise serializers.ValidationError("优惠券已使用")
        
        if user_coupon.is_expired:
            raise serializers.ValidationError("优惠券已过期")
        
        coupon = user_coupon.coupon
        
        # 检查最低消费金额
        if order_amount < coupon.min_amount:
            raise serializers.ValidationError(f"订单金额需满{coupon.min_amount}元")
        
        return attrs
