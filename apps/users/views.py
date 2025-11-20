from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from .models import User, UserProfile, UserLoginLog
from .serializers import (
    UserSerializer, UserCreateSerializer, WeChatLoginSerializer,
    PhoneLoginSerializer, UserUpdateSerializer, UserLoginLogSerializer,
    ChangePasswordSerializer, AvatarUploadSerializer
)


class UserRegisterView(generics.CreateAPIView):
    """用户注册"""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # 生成JWT token
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'code': 200,
            'message': '注册成功',
            'data': {
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }
        }, status=status.HTTP_201_CREATED)


class WeChatLoginView(APIView):
    """微信登录"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = WeChatLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        code = serializer.validated_data['code']
        
        # 这里应该调用微信API获取用户信息
        # 为了演示，我们使用模拟数据
        openid = f"mock_openid_{code}"
        nickname = "微信用户"
        avatar_url = "https://example.com/avatar.jpg"
        
        # 查找或创建用户
        user, created = User.objects.get_or_create(
            openid=openid,
            defaults={
                'nickname': nickname,
                'avatar_url': avatar_url,
                'username': f"wx_{openid}",
                'password': make_password(None)  # 微信用户不需要密码
            }
        )
        
        if not created:
            # 更新用户信息
            user.nickname = nickname
            user.avatar_url = avatar_url
            user.save()
        
        # 记录登录日志
        UserLoginLog.objects.create(
            user=user,
            login_ip=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            login_type='wechat'
        )
        
        # 生成JWT token
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'code': 200,
            'message': '登录成功',
            'data': {
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }
        })
    
    def get_client_ip(self, request):
        """获取客户端IP"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class PhoneLoginView(APIView):
    """手机号登录"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PhoneLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']
        
        # 这里应该验证短信验证码
        # 为了演示，我们假设验证码正确
        
        # 查找用户
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({
                'code': 400,
                'message': '用户不存在'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 记录登录日志
        UserLoginLog.objects.create(
            user=user,
            login_ip=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            login_type='phone'
        )
        
        # 生成JWT token
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'code': 200,
            'message': '登录成功',
            'data': {
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }
        })
    
    def get_client_ip(self, request):
        """获取客户端IP"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class UserProfileView(generics.RetrieveUpdateAPIView):
    """用户资料获取和更新"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class UserUpdateView(generics.UpdateAPIView):
    """用户信息更新"""
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """修改密码"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'code': 200,
            'message': '密码修改成功'
        })


class AvatarUploadView(APIView):
    """头像上传"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = AvatarUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        avatar = serializer.validated_data['avatar']
        
        # 这里应该上传到云存储，为了演示我们保存到本地
        user = request.user
        user.avatar_url = f"/media/avatars/{user.id}_{avatar.name}"
        user.save()
        
        return Response({
            'code': 200,
            'message': '头像上传成功',
            'data': {
                'avatar_url': user.avatar_url
            }
        })


class UserLoginLogView(generics.ListAPIView):
    """用户登录日志"""
    serializer_class = UserLoginLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserLoginLog.objects.filter(user=self.request.user).order_by('-created_at')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_sms_code(request):
    """发送短信验证码"""
    phone = request.data.get('phone')
    
    if not phone:
        return Response({
            'code': 400,
            'message': '手机号不能为空'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 这里应该调用短信服务发送验证码
    # 为了演示，我们返回成功
    
    return Response({
        'code': 200,
        'message': '验证码发送成功'
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def bind_phone(request):
    """绑定手机号"""
    phone = request.data.get('phone')
    code = request.data.get('code')
    
    if not phone or not code:
        return Response({
            'code': 400,
            'message': '手机号和验证码不能为空'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 这里应该验证短信验证码
    # 为了演示，我们假设验证码正确
    
    # 检查手机号是否已被绑定
    if User.objects.filter(phone=phone).exclude(id=request.user.id).exists():
        return Response({
            'code': 400,
            'message': '手机号已被绑定'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 绑定手机号
    user = request.user
    user.phone = phone
    user.save()
    
    return Response({
        'code': 200,
        'message': '手机号绑定成功'
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """用户统计信息"""
    user = request.user
    
    # 统计订单信息
    orders = user.orders.all()
    total_orders = orders.count()
    completed_orders = orders.filter(status='completed').count()
    total_amount = sum(order.final_amount for order in orders if order.status == 'completed')
    
    # 统计积分信息
    points = user.points
    
    return Response({
        'code': 200,
        'message': 'success',
        'data': {
            'total_orders': total_orders,
            'completed_orders': completed_orders,
            'total_amount': float(total_amount),
            'points': points,
            'is_vip': user.is_vip,
            'vip_expire_at': user.vip_expire_at.isoformat() if user.vip_expire_at else None
        }
    })
