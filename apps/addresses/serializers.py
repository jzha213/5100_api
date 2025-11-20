from rest_framework import serializers
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    """地址序列化器"""
    
    class Meta:
        model = Address
        fields = [
            'id', 'name', 'phone', 'province', 'city', 'district', 
            'street', 'detail_address', 'longitude', 'latitude', 
            'is_default', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate_phone(self, value):
        """验证手机号格式"""
        import re
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError("手机号格式不正确")
        return value


class AddressCreateSerializer(serializers.ModelSerializer):
    """地址创建序列化器"""
    
    class Meta:
        model = Address
        fields = [
            'name', 'phone', 'province', 'city', 'district', 
            'street', 'detail_address', 'longitude', 'latitude', 'is_default'
        ]
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate_phone(self, value):
        """验证手机号格式"""
        import re
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError("手机号格式不正确")
        return value
    
    def validate_street(self, value):
        """验证街道字段，处理数组格式"""
        if isinstance(value, list):
            return ''.join(str(item) for item in value)
        return str(value) if value is not None else ''
    
    def validate_is_default(self, value):
        """验证默认地址字段，处理数组格式"""
        if isinstance(value, list):
            return bool(value[0]) if value else False
        return bool(value)


class AddressUpdateSerializer(serializers.ModelSerializer):
    """地址更新序列化器"""
    
    class Meta:
        model = Address
        fields = [
            'name', 'phone', 'province', 'city', 'district', 
            'street', 'detail_address', 'longitude', 'latitude', 'is_default'
        ]
    
    def validate_phone(self, value):
        """验证手机号格式"""
        import re
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError("手机号格式不正确")
        return value
    
    def validate_street(self, value):
        """验证街道字段，处理数组格式"""
        if isinstance(value, list):
            return ''.join(str(item) for item in value)
        return str(value) if value is not None else ''
    
    def validate_is_default(self, value):
        """验证默认地址字段，处理数组格式"""
        if isinstance(value, list):
            return bool(value[0]) if value else False
        return bool(value)


class AddressListSerializer(serializers.ModelSerializer):
    """地址列表序列化器"""
    full_address = serializers.SerializerMethodField()
    
    class Meta:
        model = Address
        fields = [
            'id', 'name', 'phone', 'province', 'city', 'district', 
            'street', 'detail_address', 'full_address', 'is_default', 'created_at'
        ]
    
    def get_full_address(self, obj):
        """获取完整地址"""
        return f"{obj.province}{obj.city}{obj.district}{obj.street}{obj.detail_address}"
