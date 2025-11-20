from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from .models import Notification, NotificationTemplate, NotificationLog, Message
from .serializers import (
    NotificationSerializer, NotificationCreateSerializer, NotificationTemplateSerializer,
    NotificationTemplateCreateSerializer, NotificationLogSerializer, MessageSerializer,
    MessageCreateSerializer, MessageMarkReadSerializer, BulkMessageMarkReadSerializer
)


class NotificationListView(generics.ListAPIView):
    """通知列表"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        return Notification.objects.all().order_by('-created_at')


class NotificationCreateView(generics.CreateAPIView):
    """通知创建"""
    serializer_class = NotificationCreateSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        notification = serializer.save()
        
        return Response({
            'code': 200,
            'message': '通知创建成功',
            'data': NotificationSerializer(notification).data
        }, status=status.HTTP_201_CREATED)


class NotificationTemplateListView(generics.ListCreateAPIView):
    """通知模板列表"""
    permission_classes = [permissions.IsAdminUser]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NotificationTemplateCreateSerializer
        return NotificationTemplateSerializer
    
    def get_queryset(self):
        return NotificationTemplate.objects.filter(is_active=True).order_by('-created_at')


class NotificationLogListView(generics.ListAPIView):
    """通知发送日志列表"""
    serializer_class = NotificationLogSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        return NotificationLog.objects.all().order_by('-created_at')


class MessageListView(generics.ListAPIView):
    """消息列表"""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Message.objects.filter(user=self.request.user).order_by('-created_at')


class MessageCreateView(generics.CreateAPIView):
    """消息创建"""
    serializer_class = MessageCreateSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        
        return Response({
            'code': 200,
            'message': '消息创建成功',
            'data': MessageSerializer(message).data
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_message_read(request):
    """标记消息为已读"""
    serializer = MessageMarkReadSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    message = serializer.save()
    
    return Response({
        'code': 200,
        'message': '消息已标记为已读',
        'data': MessageSerializer(message).data
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def bulk_mark_messages_read(request):
    """批量标记消息为已读"""
    serializer = BulkMessageMarkReadSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    messages = serializer.save()
    
    return Response({
        'code': 200,
        'message': f'已标记{len(messages)}条消息为已读'
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def message_stats(request):
    """消息统计"""
    user = request.user
    
    # 统计消息数量
    total_messages = Message.objects.filter(user=user).count()
    unread_messages = Message.objects.filter(user=user, is_read=False).count()
    read_messages = Message.objects.filter(user=user, is_read=True).count()
    
    # 按类型统计
    message_types = {}
    for msg_type, _ in Message.MESSAGE_TYPE_CHOICES:
        count = Message.objects.filter(user=user, message_type=msg_type).count()
        message_types[msg_type] = count
    
    return Response({
        'code': 200,
        'message': 'success',
        'data': {
            'total_messages': total_messages,
            'unread_messages': unread_messages,
            'read_messages': read_messages,
            'message_types': message_types
        }
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def unread_messages(request):
    """未读消息"""
    user = request.user
    
    messages = Message.objects.filter(user=user, is_read=False).order_by('-created_at')
    serializer = MessageSerializer(messages, many=True)
    
    return Response({
        'code': 200,
        'message': 'success',
        'data': serializer.data
    })


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def send_notification(request):
    """发送通知"""
    title = request.data.get('title')
    content = request.data.get('content')
    notification_type = request.data.get('notification_type', 'system')
    target_user_ids = request.data.get('target_user_ids', [])
    
    if not title or not content:
        return Response({
            'code': 400,
            'message': '标题和内容不能为空'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 创建通知
    notification = Notification.objects.create(
        title=title,
        content=content,
        notification_type=notification_type
    )
    
    # 添加目标用户
    if target_user_ids:
        from apps.users.models import User
        users = User.objects.filter(id__in=target_user_ids)
        notification.target_users.set(users)
        
        # 创建消息记录
        for user in users:
            Message.objects.create(
                title=title,
                content=content,
                message_type=notification_type,
                user=user
            )
    
    # 标记为已发送
    notification.is_sent = True
    notification.sent_at = timezone.now()
    notification.save()
    
    return Response({
        'code': 200,
        'message': '通知发送成功'
    })


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def send_sms(request):
    """发送短信"""
    phone = request.data.get('phone')
    content = request.data.get('content')
    
    if not phone or not content:
        return Response({
            'code': 400,
            'message': '手机号和内容不能为空'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 这里应该调用短信服务API
    # 为了演示，我们模拟发送成功
    
    return Response({
        'code': 200,
        'message': '短信发送成功'
    })


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def send_wechat_message(request):
    """发送微信消息"""
    openid = request.data.get('openid')
    template_id = request.data.get('template_id')
    data = request.data.get('data', {})
    
    if not openid or not template_id:
        return Response({
            'code': 400,
            'message': 'openid和模板ID不能为空'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 这里应该调用微信消息推送API
    # 为了演示，我们模拟发送成功
    
    return Response({
        'code': 200,
        'message': '微信消息发送成功'
    })
