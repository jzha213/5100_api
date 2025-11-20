from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from .models import DeliveryPerson, Delivery, DeliveryTrack, DeliveryRating
from .serializers import (
    DeliveryPersonSerializer, DeliveryPersonCreateSerializer, DeliverySerializer,
    DeliveryUpdateSerializer, DeliveryTrackSerializer, DeliveryRatingSerializer,
    DeliveryRatingCreateSerializer, DeliveryAssignSerializer, DeliveryLocationUpdateSerializer
)


class DeliveryPersonListView(generics.ListAPIView):
    """配送员列表"""
    serializer_class = DeliveryPersonSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        return DeliveryPerson.objects.filter(is_active=True)


class DeliveryPersonCreateView(generics.CreateAPIView):
    """配送员创建"""
    serializer_class = DeliveryPersonCreateSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        delivery_person = serializer.save()
        
        return Response({
            'code': 200,
            'message': '配送员创建成功',
            'data': DeliveryPersonSerializer(delivery_person).data
        }, status=status.HTTP_201_CREATED)


class DeliveryPersonDetailView(generics.RetrieveUpdateAPIView):
    """配送员详情和更新"""
    serializer_class = DeliveryPersonSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        return DeliveryPerson.objects.all()


class DeliveryListView(generics.ListAPIView):
    """配送记录列表"""
    serializer_class = DeliverySerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        return Delivery.objects.all().order_by('-created_at')


class DeliveryDetailView(generics.RetrieveUpdateAPIView):
    """配送详情和更新"""
    serializer_class = DeliveryUpdateSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        return Delivery.objects.all()
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return DeliveryUpdateSerializer
        return DeliverySerializer


class DeliveryTrackListView(generics.ListAPIView):
    """配送轨迹列表"""
    serializer_class = DeliveryTrackSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        delivery_id = self.kwargs['delivery_id']
        return DeliveryTrack.objects.filter(delivery_id=delivery_id).order_by('-created_at')


class DeliveryRatingListView(generics.ListAPIView):
    """配送评价列表"""
    serializer_class = DeliveryRatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        delivery_id = self.kwargs['delivery_id']
        return DeliveryRating.objects.filter(delivery_id=delivery_id).order_by('-created_at')


class DeliveryRatingCreateView(generics.CreateAPIView):
    """配送评价创建"""
    serializer_class = DeliveryRatingCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating = serializer.save()
        
        return Response({
            'code': 200,
            'message': '评价提交成功',
            'data': DeliveryRatingSerializer(rating).data
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def assign_delivery(request):
    """分配配送员"""
    serializer = DeliveryAssignSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    delivery_id = serializer.validated_data['delivery_id']
    delivery_person_id = serializer.validated_data['delivery_person_id']
    
    delivery = Delivery.objects.get(id=delivery_id)
    delivery_person = DeliveryPerson.objects.get(id=delivery_person_id)
    
    # 更新配送记录
    old_status = delivery.status
    delivery.delivery_person = delivery_person
    delivery.status = 'assigned'
    delivery.assigned_at = timezone.now()
    delivery.save()
    
    # 记录配送轨迹
    DeliveryTrack.objects.create(
        delivery=delivery,
        status='assigned',
        remark=f"已分配给配送员: {delivery_person.name}"
    )
    
    return Response({
        'code': 200,
        'message': '配送员分配成功',
        'data': DeliverySerializer(delivery).data
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_delivery_location(request):
    """更新配送员位置"""
    # 这里应该验证是配送员本人
    # 为了演示，我们简化处理
    
    serializer = DeliveryLocationUpdateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    latitude = serializer.validated_data['latitude']
    longitude = serializer.validated_data['longitude']
    
    # 这里应该根据用户身份找到对应的配送员
    # 为了演示，我们假设request.user是配送员
    try:
        delivery_person = DeliveryPerson.objects.get(phone=request.user.phone)
    except DeliveryPerson.DoesNotExist:
        return Response({
            'code': 403,
            'message': '您不是配送员'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # 更新配送员位置
    delivery_person.current_latitude = latitude
    delivery_person.current_longitude = longitude
    delivery_person.last_update_location = timezone.now()
    delivery_person.save()
    
    return Response({
        'code': 200,
        'message': '位置更新成功'
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def delivery_track(request, order_id):
    """订单配送轨迹"""
    try:
        from apps.orders.models import Order
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return Response({
            'code': 404,
            'message': '订单不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    
    try:
        delivery = order.delivery
    except:
        return Response({
            'code': 404,
            'message': '配送记录不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # 获取配送轨迹
    tracks = DeliveryTrack.objects.filter(delivery=delivery).order_by('created_at')
    track_serializer = DeliveryTrackSerializer(tracks, many=True)
    
    # 获取配送员信息
    delivery_serializer = DeliverySerializer(delivery)
    
    return Response({
        'code': 200,
        'message': 'success',
        'data': {
            'delivery': delivery_serializer.data,
            'tracks': track_serializer.data
        }
    })


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def delivery_stats(request):
    """配送统计"""
    # 今日配送统计
    today = timezone.now().date()
    today_deliveries = Delivery.objects.filter(created_at__date=today)
    
    # 配送员统计
    delivery_persons = DeliveryPerson.objects.filter(is_active=True)
    
    stats = {
        'today_total': today_deliveries.count(),
        'today_completed': today_deliveries.filter(status='completed').count(),
        'today_delivering': today_deliveries.filter(status='delivering').count(),
        'delivery_persons_count': delivery_persons.count(),
        'online_delivery_persons': delivery_persons.filter(status=1).count(),
    }
    
    return Response({
        'code': 200,
        'message': 'success',
        'data': stats
    })
