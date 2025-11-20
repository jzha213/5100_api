from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from .models import Coupon, UserCoupon, CouponUsage
from .serializers import (
    CouponSerializer, CouponCreateSerializer, UserCouponSerializer,
    UserCouponCreateSerializer, CouponUsageSerializer, CouponValidateSerializer
)


class CouponListView(generics.ListAPIView):
    """优惠券列表"""
    serializer_class = CouponSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return Coupon.objects.filter(is_active=True, valid_from__lte=timezone.now(), valid_to__gte=timezone.now())


class CouponCreateView(generics.CreateAPIView):
    """优惠券创建"""
    serializer_class = CouponCreateSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        coupon = serializer.save()
        
        return Response({
            'code': 200,
            'message': '优惠券创建成功',
            'data': CouponSerializer(coupon).data
        }, status=status.HTTP_201_CREATED)


class UserCouponListView(generics.ListAPIView):
    """用户优惠券列表"""
    serializer_class = UserCouponSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserCoupon.objects.filter(user=self.request.user).order_by('-created_at')


class UserCouponCreateView(generics.CreateAPIView):
    """用户领取优惠券"""
    serializer_class = UserCouponCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_coupon = serializer.save()
        
        return Response({
            'code': 200,
            'message': '优惠券领取成功',
            'data': UserCouponSerializer(user_coupon).data
        }, status=status.HTTP_201_CREATED)


class CouponUsageListView(generics.ListAPIView):
    """优惠券使用记录"""
    serializer_class = CouponUsageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CouponUsage.objects.filter(user_coupon__user=self.request.user).order_by('-created_at')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def validate_coupon(request):
    """验证优惠券"""
    serializer = CouponValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    coupon_code = serializer.validated_data['coupon_code']
    order_amount = serializer.validated_data['order_amount']
    
    # 获取用户优惠券
    user_coupon = UserCoupon.objects.get(
        user=request.user,
        coupon__name=coupon_code
    )
    
    coupon = user_coupon.coupon
    
    # 计算优惠金额
    discount_amount = 0
    if coupon.coupon_type == 'discount':
        discount_amount = order_amount * (coupon.discount_rate / 100)
        if coupon.max_discount and discount_amount > coupon.max_discount:
            discount_amount = coupon.max_discount
    elif coupon.coupon_type == 'cash':
        discount_amount = coupon.discount_value
    elif coupon.coupon_type == 'free_shipping':
        # 这里应该获取配送费，为了演示设为10元
        discount_amount = 10
    
    return Response({
        'code': 200,
        'message': '优惠券验证成功',
        'data': {
            'coupon_name': coupon.name,
            'discount_amount': float(discount_amount),
            'final_amount': float(order_amount - discount_amount)
        }
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def available_coupons(request):
    """可用优惠券"""
    user = request.user
    
    # 获取用户未使用的优惠券
    user_coupons = UserCoupon.objects.filter(
        user=user,
        status='unused'
    ).exclude(
        expired_at__lt=timezone.now()
    ).order_by('-created_at')
    
    serializer = UserCouponSerializer(user_coupons, many=True)
    
    return Response({
        'code': 200,
        'message': 'success',
        'data': serializer.data
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def coupon_stats(request):
    """优惠券统计"""
    user = request.user
    
    # 统计用户优惠券
    total_coupons = UserCoupon.objects.filter(user=user).count()
    unused_coupons = UserCoupon.objects.filter(user=user, status='unused').count()
    used_coupons = UserCoupon.objects.filter(user=user, status='used').count()
    expired_coupons = UserCoupon.objects.filter(user=user, status='expired').count()
    
    # 统计优惠金额
    total_discount = sum(
        usage.discount_amount for usage in 
        CouponUsage.objects.filter(user_coupon__user=user)
    )
    
    return Response({
        'code': 200,
        'message': 'success',
        'data': {
            'total_coupons': total_coupons,
            'unused_coupons': unused_coupons,
            'used_coupons': used_coupons,
            'expired_coupons': expired_coupons,
            'total_discount': float(total_discount)
        }
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def use_coupon(request):
    """使用优惠券"""
    coupon_code = request.data.get('coupon_code')
    order_id = request.data.get('order_id')
    
    if not coupon_code or not order_id:
        return Response({
            'code': 400,
            'message': '优惠券代码和订单ID不能为空'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        from apps.orders.models import Order
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return Response({
            'code': 404,
            'message': '订单不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    
    try:
        user_coupon = UserCoupon.objects.get(
            user=request.user,
            coupon__name=coupon_code,
            status='unused'
        )
    except UserCoupon.DoesNotExist:
        return Response({
            'code': 404,
            'message': '优惠券不存在或已使用'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if user_coupon.is_expired:
        return Response({
            'code': 400,
            'message': '优惠券已过期'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    coupon = user_coupon.coupon
    
    # 检查最低消费金额
    if order.total_amount < coupon.min_amount:
        return Response({
            'code': 400,
            'message': f'订单金额需满{coupon.min_amount}元'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 计算优惠金额
    discount_amount = 0
    if coupon.coupon_type == 'discount':
        discount_amount = order.total_amount * (coupon.discount_rate / 100)
        if coupon.max_discount and discount_amount > coupon.max_discount:
            discount_amount = coupon.max_discount
    elif coupon.coupon_type == 'cash':
        discount_amount = coupon.discount_value
    elif coupon.coupon_type == 'free_shipping':
        discount_amount = order.shipping_fee
    
    # 更新订单优惠金额
    order.discount_amount = discount_amount
    order.final_amount = order.total_amount - discount_amount + order.shipping_fee
    order.save()
    
    # 标记优惠券为已使用
    user_coupon.status = 'used'
    user_coupon.used_at = timezone.now()
    user_coupon.used_order = order
    user_coupon.save()
    
    # 记录使用记录
    CouponUsage.objects.create(
        user_coupon=user_coupon,
        order=order,
        discount_amount=discount_amount
    )
    
    # 更新优惠券使用次数
    coupon.used_count += 1
    coupon.save()
    
    return Response({
        'code': 200,
        'message': '优惠券使用成功',
        'data': {
            'discount_amount': float(discount_amount),
            'final_amount': float(order.final_amount)
        }
    })
