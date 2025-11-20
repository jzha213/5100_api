from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Address
from .serializers import (
    AddressSerializer, AddressCreateSerializer, AddressUpdateSerializer,
    AddressListSerializer
)


class AddressListView(generics.ListCreateAPIView):
    """地址列表和创建"""
    serializer_class = AddressListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddressCreateSerializer
        return AddressListSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'code': 200,
            'message': 'success',
            'data': serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({
            'code': 200,
            'message': '地址创建成功',
            'data': AddressSerializer(serializer.instance).data
        }, status=status.HTTP_201_CREATED)


class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    """地址详情、更新和删除"""
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AddressUpdateSerializer
        return AddressSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        return Response({
            'code': 200,
            'message': 'success',
            'data': serializer.data
        })
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'code': 200,
            'message': '地址更新成功',
            'data': AddressSerializer(serializer.instance).data
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return Response({
            'code': 200,
            'message': '地址删除成功'
        })


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def set_default_address(request, address_id):
    """设置默认地址"""
    try:
        address = Address.objects.get(id=address_id, user=request.user)
    except Address.DoesNotExist:
        return Response({
            'code': 404,
            'message': '地址不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # 取消其他默认地址
    Address.objects.filter(user=request.user, is_default=True).update(is_default=False)
    
    # 设置当前地址为默认
    address.is_default = True
    address.save()
    
    return Response({
        'code': 200,
        'message': '默认地址设置成功'
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_default_address(request):
    """获取默认地址"""
    try:
        address = Address.objects.get(user=request.user, is_default=True)
        serializer = AddressSerializer(address)
        
        return Response({
            'code': 200,
            'message': 'success',
            'data': serializer.data
        })
    except Address.DoesNotExist:
        return Response({
            'code': 404,
            'message': '暂无默认地址'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_address_by_location(request):
    """根据位置获取地址信息"""
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')
    
    if not latitude or not longitude:
        return Response({
            'code': 400,
            'message': '经纬度不能为空'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        lat = float(latitude)
        lng = float(longitude)
    except ValueError:
        return Response({
            'code': 400,
            'message': '经纬度格式不正确'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 这里应该调用地图API获取地址信息
    # 为了演示，我们返回模拟数据
    
    address_info = {
        'province': '北京市',
        'city': '北京市',
        'district': '朝阳区',
        'street': '三里屯街道',
        'detail_address': '三里屯SOHO',
        'formatted_address': '北京市朝阳区三里屯街道三里屯SOHO'
    }
    
    return Response({
        'code': 200,
        'message': 'success',
        'data': address_info
    })
