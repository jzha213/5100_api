from django.urls import path, include
from . import views

app_name = 'users'

# 认证相关URL
auth_urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('wechat/login/', views.WeChatLoginView.as_view(), name='wechat-login'),
    path('phone/login/', views.PhoneLoginView.as_view(), name='phone-login'),
]

# 用户相关URL
users_urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('update/', views.UserUpdateView.as_view(), name='update'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('avatar/upload/', views.AvatarUploadView.as_view(), name='avatar-upload'),
    path('login-logs/', views.UserLoginLogView.as_view(), name='login-logs'),
    path('send-sms/', views.send_sms_code, name='send-sms'),
    path('bind-phone/', views.bind_phone, name='bind-phone'),
    path('stats/', views.user_stats, name='stats'),
]

urlpatterns = [
    path('auth/', include(auth_urlpatterns)),
    path('', include(users_urlpatterns)),
]
