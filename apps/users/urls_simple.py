from django.urls import path
from . import views_simple, upload_views

app_name = 'users'

urlpatterns = [
    # 认证相关
    path('login/', views_simple.login, name='login'),
    path('register/', views_simple.register, name='register'),
    path('logout/', views_simple.logout, name='logout'),
    path('refresh/', views_simple.refresh_token, name='refresh-token'),
    
    # 用户信息
    path('profile/', views_simple.user_profile, name='user-profile'),
    
    # 文件上传
    path('upload/avatar/', upload_views.upload_avatar, name='upload-avatar'),
]
