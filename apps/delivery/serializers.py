from rest_framework import serializers
from .models import DeliveryPerson, Delivery, DeliveryTrack, DeliveryRating


class DeliveryPersonSerializer(serializers.ModelSerializer):
    """配送员序列化器"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = DeliveryPerson
        fields = [
            'id', 'name', 'phone', 'status', 'status_display', 'is_active',
            'total_orders', 'completed_orders', 'rating', 'current_latitude',
            'current_longitude', 'last_update_location', 'created_at'
        ]
        read_only_fields = ['id', 'total_orders', 'completed_orders', 'rating', 'created_at']


class DeliveryPersonCreateSerializer(serializers.ModelSerializer):
    """配送员创建序列化器"""
    
    class Meta:
        model = DeliveryPerson
        fields = ['name', 'phone', 'id_card']
    
    def validate_phone(self, value):
        """验证手机号格式"""
        import re
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError("手机号格式不正确")
        return value


class DeliveryTrackSerializer(serializers.ModelSerializer):
    """配送轨迹序列化器"""
    
    class Meta:
        model = DeliveryTrack
        fields = [
            'id', 'status', 'latitude', 'longitude', 'address', 
            'remark', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class DeliveryRatingSerializer(serializers.ModelSerializer):
    """配送评价序列化器"""
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    
    class Meta:
        model = DeliveryRating
        fields = ['id', 'user_nickname', 'rating', 'content', 'created_at']
        read_only_fields = ['id', 'user_nickname', 'created_at']


class DeliveryRatingCreateSerializer(serializers.ModelSerializer):
    """配送评价创建序列化器"""
    
    class Meta:
        model = DeliveryRating
        fields = ['delivery', 'rating', 'content']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['delivery_person'] = validated_data['delivery'].delivery_person
        return super().create(validated_data)


class DeliverySerializer(serializers.ModelSerializer):
    """配送记录序列化器"""
    order_no = serializers.CharField(source='order.order_no', read_only=True)
    delivery_person_name = serializers.CharField(source='delivery_person.name', read_only=True)
    delivery_person_phone = serializers.CharField(source='delivery_person.phone', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    tracks = DeliveryTrackSerializer(many=True, read_only=True)
    rating = DeliveryRatingSerializer(read_only=True)
    
    class Meta:
        model = Delivery
        fields = [
            'id', 'delivery_no', 'order_no', 'delivery_person', 'delivery_person_name',
            'delivery_person_phone', 'status', 'status_display', 'delivery_address',
            'contact_name', 'contact_phone', 'assigned_at', 'accepted_at',
            'picked_up_at', 'delivered_at', 'completed_at', 'remark',
            'tracks', 'rating', 'created_at'
        ]


class DeliveryUpdateSerializer(serializers.ModelSerializer):
    """配送更新序列化器"""
    
    class Meta:
        model = Delivery
        fields = ['status', 'remark']
    
    def update(self, instance, validated_data):
        old_status = instance.status
        new_status = validated_data.get('status', instance.status)
        
        # 更新配送状态
        instance = super().update(instance, validated_data)
        
        # 记录状态变更日志
        if old_status != new_status:
            from apps.orders.models import OrderStatusLog
            OrderStatusLog.objects.create(
                order=instance.order,
                from_status=old_status,
                to_status=new_status,
                operator=self.context['request'].user,
                remark=f"配送状态变更: {instance.get_status_display()}"
            )
        
        return instance


class DeliveryAssignSerializer(serializers.Serializer):
    """配送分配序列化器"""
    delivery_id = serializers.IntegerField()
    delivery_person_id = serializers.IntegerField()
    
    def validate_delivery_id(self, value):
        """验证配送ID"""
        try:
            delivery = Delivery.objects.get(id=value)
        except Delivery.DoesNotExist:
            raise serializers.ValidationError("配送记录不存在")
        
        if delivery.status != 'pending':
            raise serializers.ValidationError("配送状态不正确")
        
        return value
    
    def validate_delivery_person_id(self, value):
        """验证配送员ID"""
        try:
            delivery_person = DeliveryPerson.objects.get(id=value)
        except DeliveryPerson.DoesNotExist:
            raise serializers.ValidationError("配送员不存在")
        
        if not delivery_person.is_active:
            raise serializers.ValidationError("配送员未启用")
        
        if delivery_person.status == 3:  # 休假
            raise serializers.ValidationError("配送员正在休假")
        
        return value
    
    def validate(self, attrs):
        """验证配送分配"""
        delivery_id = attrs['delivery_id']
        delivery_person_id = attrs['delivery_person_id']
        
        delivery = Delivery.objects.get(id=delivery_id)
        delivery_person = DeliveryPerson.objects.get(id=delivery_person_id)
        
        # 检查配送员是否已有未完成的配送任务
        active_deliveries = delivery_person.deliveries.filter(
            status__in=['assigned', 'accepted', 'picked_up', 'delivering']
        ).count()
        
        if active_deliveries >= 5:  # 假设每个配送员最多同时处理5个订单
            raise serializers.ValidationError("配送员任务已满")
        
        return attrs


class DeliveryLocationUpdateSerializer(serializers.Serializer):
    """配送员位置更新序列化器"""
    latitude = serializers.DecimalField(max_digits=10, decimal_places=7)
    longitude = serializers.DecimalField(max_digits=10, decimal_places=7)
    
    def validate_latitude(self, value):
        """验证纬度"""
        if not (-90 <= value <= 90):
            raise serializers.ValidationError("纬度必须在-90到90之间")
        return value
    
    def validate_longitude(self, value):
        """验证经度"""
        if not (-180 <= value <= 180):
            raise serializers.ValidationError("经度必须在-180到180之间")
        return value
