from rest_framework import serializers
from .models import Notification, NotificationTemplate, NotificationLog, Message


class NotificationSerializer(serializers.ModelSerializer):
    """通知序列化器"""
    notification_type_display = serializers.CharField(source='get_notification_type_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    target_users_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'title', 'content', 'notification_type', 'notification_type_display',
            'priority', 'priority_display', 'target_users_count', 'related_order',
            'related_url', 'is_sent', 'sent_at', 'scheduled_at', 'expires_at',
            'created_at'
        ]
    
    def get_target_users_count(self, obj):
        """获取目标用户数量"""
        return obj.target_users.count()


class NotificationCreateSerializer(serializers.ModelSerializer):
    """通知创建序列化器"""
    target_user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Notification
        fields = [
            'title', 'content', 'notification_type', 'priority', 'target_user_ids',
            'related_order', 'related_url', 'scheduled_at', 'expires_at'
        ]
    
    def create(self, validated_data):
        target_user_ids = validated_data.pop('target_user_ids', [])
        
        # 创建通知
        notification = Notification.objects.create(**validated_data)
        
        # 添加目标用户
        if target_user_ids:
            from apps.users.models import User
            users = User.objects.filter(id__in=target_user_ids)
            notification.target_users.set(users)
        
        return notification


class NotificationTemplateSerializer(serializers.ModelSerializer):
    """通知模板序列化器"""
    template_type_display = serializers.CharField(source='get_template_type_display', read_only=True)
    
    class Meta:
        model = NotificationTemplate
        fields = [
            'id', 'name', 'template_type', 'template_type_display', 'title_template',
            'content_template', 'variables', 'is_active', 'created_at'
        ]


class NotificationTemplateCreateSerializer(serializers.ModelSerializer):
    """通知模板创建序列化器"""
    
    class Meta:
        model = NotificationTemplate
        fields = [
            'name', 'template_type', 'title_template', 'content_template',
            'variables', 'is_active'
        ]


class NotificationLogSerializer(serializers.ModelSerializer):
    """通知发送日志序列化器"""
    notification_title = serializers.CharField(source='notification.title', read_only=True)
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = NotificationLog
        fields = [
            'id', 'notification_title', 'user_nickname', 'channel', 'status',
            'status_display', 'third_party_id', 'sent_at', 'delivered_at',
            'error_message', 'created_at'
        ]


class MessageSerializer(serializers.ModelSerializer):
    """消息序列化器"""
    message_type_display = serializers.CharField(source='get_message_type_display', read_only=True)
    related_order_no = serializers.CharField(source='related_order.order_no', read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'id', 'title', 'content', 'message_type', 'message_type_display',
            'is_read', 'read_at', 'related_order_no', 'created_at'
        ]
        read_only_fields = ['id', 'is_read', 'read_at', 'created_at']


class MessageCreateSerializer(serializers.ModelSerializer):
    """消息创建序列化器"""
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Message
        fields = [
            'title', 'content', 'message_type', 'user_id', 'related_order'
        ]
    
    def validate_user_id(self, value):
        """验证用户ID"""
        from apps.users.models import User
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("用户不存在")
        return value
    
    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        
        from apps.users.models import User
        user = User.objects.get(id=user_id)
        
        message = Message.objects.create(
            user=user,
            **validated_data
        )
        
        return message


class MessageMarkReadSerializer(serializers.Serializer):
    """消息标记为已读序列化器"""
    message_id = serializers.IntegerField()
    
    def validate_message_id(self, value):
        """验证消息ID"""
        user = self.context['request'].user
        try:
            message = user.messages.get(id=value)
        except Message.DoesNotExist:
            raise serializers.ValidationError("消息不存在")
        return value
    
    def save(self):
        """标记消息为已读"""
        from django.utils import timezone
        
        message_id = self.validated_data['message_id']
        user = self.context['request'].user
        
        message = user.messages.get(id=message_id)
        message.is_read = True
        message.read_at = timezone.now()
        message.save()
        
        return message


class BulkMessageMarkReadSerializer(serializers.Serializer):
    """批量标记消息为已读序列化器"""
    message_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1
    )
    
    def validate_message_ids(self, value):
        """验证消息ID列表"""
        user = self.context['request'].user
        messages = user.messages.filter(id__in=value)
        
        if len(messages) != len(value):
            raise serializers.ValidationError("部分消息不存在")
        
        return value
    
    def save(self):
        """批量标记消息为已读"""
        from django.utils import timezone
        
        message_ids = self.validated_data['message_ids']
        user = self.context['request'].user
        
        user.messages.filter(id__in=message_ids).update(
            is_read=True,
            read_at=timezone.now()
        )
        
        return user.messages.filter(id__in=message_ids)
