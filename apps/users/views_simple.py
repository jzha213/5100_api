from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """用户登录API"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'success': False,
            'message': '用户名和密码不能为空'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 尝试用户名登录
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response({
            'success': False,
            'message': '用户名或密码错误'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # 生成JWT token
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    
    return Response({
        'success': True,
        'message': '登录成功',
        'data': {
            'user': UserSerializer(user).data,
            'access_token': str(access_token),
            'refresh_token': str(refresh)
        }
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """用户注册API"""
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    phone = request.data.get('phone')
    nickname = request.data.get('nickname', '')
    
    if not username or not password:
        return Response({
            'success': False,
            'message': '用户名和密码不能为空'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 检查用户是否已存在
    if User.objects.filter(username=username).exists():
        return Response({
            'success': False,
            'message': '用户名已存在'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 检查邮箱是否已存在
    if email and User.objects.filter(email=email).exists():
        return Response({
            'success': False,
            'message': '邮箱已存在'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 检查手机号是否已存在
    if phone and User.objects.filter(phone=phone).exists():
        return Response({
            'success': False,
            'message': '手机号已存在'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 创建用户
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email or '',
        phone=phone or '',
        nickname=nickname
    )
    
    return Response({
        'success': True,
        'message': '注册成功',
        'data': UserSerializer(user).data
    })

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """获取/更新用户信息API"""
    if request.method == 'GET':
        return Response({
            'success': True,
            'data': UserSerializer(request.user).data
        })
    
    elif request.method == 'PUT':
        user = request.user
        data = request.data
        
        # 验证用户名格式（只允许英文和数字）
        new_username = data.get('username')
        if new_username:
            import re
            if not re.match(r'^[a-zA-Z0-9]+$', new_username):
                return Response({
                    'success': False,
                    'message': '此账号包含非法字符，只能使用英文和数字'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 检查用户名是否已被其他用户使用
            if User.objects.filter(username=new_username).exclude(id=user.id).exists():
                return Response({
                    'success': False,
                    'message': '此账号已被使用，请更换一个'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证密码
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        if old_password and new_password:
            if not user.check_password(old_password):
                return Response({
                    'success': False,
                    'message': '原密码输入错误'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if len(new_password) < 6:
                return Response({
                    'success': False,
                    'message': '新密码长度不能少于6位'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证邮箱格式
        email = data.get('email')
        if email:
            import re
            if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
                return Response({
                    'success': False,
                    'message': '邮箱格式不正确'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 检查邮箱是否已被其他用户使用
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                return Response({
                    'success': False,
                    'message': '邮箱已被使用'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证手机号格式
        phone = data.get('phone')
        if phone:
            if not re.match(r'^1[3-9]\d{9}$', phone):
                return Response({
                    'success': False,
                    'message': '手机号格式不正确'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 检查手机号是否已被其他用户使用
            if User.objects.filter(phone=phone).exclude(id=user.id).exists():
                return Response({
                    'success': False,
                    'message': '手机号已被使用'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # 更新用户信息
        try:
            if new_username:
                user.username = new_username
            
            if new_password:
                user.set_password(new_password)
            
            if 'nickname' in data:
                user.nickname = data.get('nickname', '')
            
            if 'avatar_url' in data:
                user.avatar_url = data.get('avatar_url', '')
            
            if email is not None:
                user.email = email
            
            if phone is not None:
                user.phone = phone
            
            user.save()
            
            return Response({
                'success': True,
                'message': '用户信息更新成功',
                'data': UserSerializer(user).data
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'更新失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refresh_token(request):
    """刷新token API"""
    refresh_token = request.data.get('refresh_token')
    
    if not refresh_token:
        return Response({
            'success': False,
            'message': 'refresh_token不能为空'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        refresh = RefreshToken(refresh_token)
        access_token = refresh.access_token
        
        return Response({
            'success': True,
            'data': {
                'access_token': str(access_token),
                'refresh_token': str(refresh)
            }
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': 'token无效或已过期'
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """用户登出API"""
    return Response({
        'success': True,
        'message': '登出成功'
    })
