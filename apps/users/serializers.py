from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, UserProfile, UserLoginLog


class UserProfileSerializer(serializers.ModelSerializer):
    """用户资料序列化器"""
    
    class Meta:
        model = UserProfile
        fields = ['real_name', 'id_card', 'address', 'emergency_contact', 'emergency_phone']


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'nickname', 'avatar_url', 'phone', 'gender', 
            'birthday', 'is_vip', 'vip_expire_at', 'points', 'total_consumption',
            'status', 'created_at', 'profile'
        ]
        read_only_fields = ['id', 'created_at', 'points', 'total_consumption']


class UserCreateSerializer(serializers.ModelSerializer):
    """用户创建序列化器"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'nickname', 'phone', 'password', 'password_confirm']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("密码不匹配")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class WeChatLoginSerializer(serializers.Serializer):
    """微信登录序列化器"""
    code = serializers.CharField(max_length=100)
    encrypted_data = serializers.CharField(required=False)
    iv = serializers.CharField(required=False)
    
    def validate_code(self, value):
        if not value:
            raise serializers.ValidationError("微信授权码不能为空")
        return value


class PhoneLoginSerializer(serializers.Serializer):
    """手机号登录序列化器"""
    phone = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=6)
    
    def validate_phone(self, value):
        if not value:
            raise serializers.ValidationError("手机号不能为空")
        return value
    
    def validate_code(self, value):
        if not value:
            raise serializers.ValidationError("验证码不能为空")
        return value


class UserUpdateSerializer(serializers.ModelSerializer):
    """用户更新序列化器"""
    profile = UserProfileSerializer()
    
    class Meta:
        model = User
        fields = ['nickname', 'avatar_url', 'gender', 'birthday', 'profile']
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        
        # 更新用户信息
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # 更新用户资料
        if profile_data:
            profile, created = UserProfile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        return instance


class UserLoginLogSerializer(serializers.ModelSerializer):
    """用户登录日志序列化器"""
    
    class Meta:
        model = UserLoginLog
        fields = ['login_ip', 'user_agent', 'login_type', 'created_at']
        read_only_fields = ['created_at']


class ChangePasswordSerializer(serializers.Serializer):
    """修改密码序列化器"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("新密码不匹配")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("原密码错误")
        return value
    
    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class AvatarUploadSerializer(serializers.Serializer):
    """头像上传序列化器"""
    avatar = serializers.ImageField()
    
    def validate_avatar(self, value):
        # 检查文件大小 (限制为5MB)
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("头像文件大小不能超过5MB")
        
        # 检查文件格式
        allowed_formats = ['JPEG', 'JPG', 'PNG']
        if value.image.format not in allowed_formats:
            raise serializers.ValidationError("头像格式必须是JPEG、JPG或PNG")
        
        return value
