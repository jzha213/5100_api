from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # 通知相关
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('create/', views.NotificationCreateView.as_view(), name='notification-create'),
    path('send/', views.send_notification, name='send-notification'),
    
    # 通知模板相关
    path('templates/', views.NotificationTemplateListView.as_view(), name='notification-template-list'),
    
    # 通知日志
    path('logs/', views.NotificationLogListView.as_view(), name='notification-log-list'),
    
    # 消息相关
    path('messages/', views.MessageListView.as_view(), name='message-list'),
    path('messages/create/', views.MessageCreateView.as_view(), name='message-create'),
    path('messages/mark-read/', views.mark_message_read, name='mark-message-read'),
    path('messages/bulk-mark-read/', views.bulk_mark_messages_read, name='bulk-mark-messages-read'),
    path('messages/stats/', views.message_stats, name='message-stats'),
    path('messages/unread/', views.unread_messages, name='unread-messages'),
    
    # 发送相关
    path('send/sms/', views.send_sms, name='send-sms'),
    path('send/wechat/', views.send_wechat_message, name='send-wechat-message'),
]
