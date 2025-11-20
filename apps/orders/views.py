from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Order, OrderItem, Cart, OrderStatusLog
from .serializers import (
    OrderListSerializer, OrderDetailSerializer, OrderCreateSerializer,
    OrderUpdateSerializer, CartSerializer, CartCreateSerializer, CartUpdateSerializer
)


class OrderListView(generics.ListAPIView):
    """订单列表"""
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'payment_status']
    search_fields = ['order_no']
    ordering_fields = ['created_at', 'final_amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(generics.RetrieveAPIView):
    """订单详情"""
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreateView(generics.CreateAPIView):
    """订单创建"""
    serializer_class = OrderCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        # 注意：不再自动清空购物车，让前端决定是否删除已结算的商品
        # 这样可以支持部分结算，用户可以选择只结算部分商品
        
        return Response({
            'code': 200,
            'message': '订单创建成功',
            'data': OrderDetailSerializer(order).data
        }, status=status.HTTP_201_CREATED)


class OrderUpdateView(generics.UpdateAPIView):
    """订单更新"""
    serializer_class = OrderUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDestroyView(generics.DestroyAPIView):
    """订单删除"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # 只有待支付状态的订单才能删除
        if instance.status not in ['pending', 'unpaid']:
            return Response({
                'code': 400,
                'message': '只有待支付状态的订单才能删除'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 记录删除日志
        OrderStatusLog.objects.create(
            order=instance,
            from_status=instance.status,
            to_status='deleted',
            operator=request.user,
            remark="用户删除订单"
        )
        
        self.perform_destroy(instance)
        
        return Response({
            'code': 200,
            'message': '订单删除成功'
        })
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # 记录状态变更
        old_status = instance.status
        old_payment_status = instance.payment_status
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # 记录状态变更日志
        new_status = serializer.instance.status
        new_payment_status = serializer.instance.payment_status
        
        if old_status != new_status:
            OrderStatusLog.objects.create(
                order=instance,
                from_status=old_status,
                to_status=new_status,
                operator=request.user,
                remark=f"订单状态变更: {instance.get_status_display()}"
            )
        
        if old_payment_status != new_payment_status:
            OrderStatusLog.objects.create(
                order=instance,
                from_status=old_payment_status,
                to_status=new_payment_status,
                operator=request.user,
                remark=f"支付状态变更: {instance.get_payment_status_display()}"
            )
        
        return Response({
            'code': 200,
            'message': '订单更新成功',
            'data': OrderDetailSerializer(serializer.instance).data
        })


class CartListView(generics.ListAPIView):
    """购物车列表"""
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartCreateView(generics.CreateAPIView):
    """购物车添加商品"""
    serializer_class = CartCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart_item = serializer.save()
        
        return Response({
            'code': 200,
            'message': '已添加到购物车',
            'data': CartSerializer(cart_item).data
        }, status=status.HTTP_201_CREATED)


class CartUpdateView(generics.UpdateAPIView):
    """购物车更新"""
    serializer_class = CartUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'code': 200,
            'message': '购物车更新成功',
            'data': CartSerializer(serializer.instance).data
        })


class CartDestroyView(generics.DestroyAPIView):
    """购物车删除"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return Response({
            'code': 200,
            'message': '商品已从购物车移除'
        })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def cancel_order(request, order_id):
    """取消订单"""
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return Response({
            'code': 404,
            'message': '订单不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if order.status not in ['pending', 'paid']:
        return Response({
            'code': 400,
            'message': '订单状态不允许取消'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    cancel_reason = request.data.get('cancel_reason', '用户取消')
    
    # 更新订单状态
    old_status = order.status
    order.status = 'cancelled'
    order.cancel_reason = cancel_reason
    order.save()
    
    # 记录状态变更日志
    OrderStatusLog.objects.create(
        order=order,
        from_status=old_status,
        to_status='cancelled',
        operator=request.user,
        remark=f"订单取消: {cancel_reason}"
    )
    
    return Response({
        'code': 200,
        'message': '订单取消成功'
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def confirm_order(request, order_id):
    """确认收货"""
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return Response({
            'code': 404,
            'message': '订单不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if order.status != 'delivered':
        return Response({
            'code': 400,
            'message': '订单状态不允许确认收货'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 更新订单状态
    old_status = order.status
    order.status = 'completed'
    order.completed_time = timezone.now()
    order.save()
    
    # 记录状态变更日志
    OrderStatusLog.objects.create(
        order=order,
        from_status=old_status,
        to_status='completed',
        operator=request.user,
        remark="用户确认收货"
    )
    
    return Response({
        'code': 200,
        'message': '订单确认收货成功'
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def cart_summary(request):
    """购物车汇总"""
    cart_items = Cart.objects.filter(user=request.user)
    
    total_items = sum(item.quantity for item in cart_items)
    total_amount = sum(item.subtotal for item in cart_items)
    
    return Response({
        'code': 200,
        'message': 'success',
        'data': {
            'total_items': total_items,
            'total_amount': float(total_amount),
            'items_count': cart_items.count()
        }
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def clear_cart(request):
    """清空购物车"""
    Cart.objects.filter(user=request.user).delete()
    
    return Response({
        'code': 200,
        'message': '购物车已清空'
    })
