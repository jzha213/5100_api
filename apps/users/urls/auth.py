from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('wechat/login/', views.WeChatLoginView.as_view(), name='wechat-login'),
    path('phone/login/', views.PhoneLoginView.as_view(), name='phone-login'),
]
