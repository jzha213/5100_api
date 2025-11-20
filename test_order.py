#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()

def test_order_creation():
    """测试订单创建"""
    client = Client()
    
    try:
        # 获取admin用户
        user = User.objects.get(username='admin')
        print(f"找到用户: {user.username}")
        
        # 创建JWT token
        token = AccessToken.for_user(user)
        
        # 设置认证头
        headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        
        # 测试数据
        order_data = {
            'address_id': 1,
            'items': [
                {
                    'product_id': 1,
                    'quantity': 1
                }
            ],
            'remark': '测试订单'
        }
        
        print(f"发送订单数据: {order_data}")
        
        # 发送POST请求
        response = client.post('/api/v1/orders/create/', 
                             data=order_data, 
                             content_type='application/json',
                             **headers)
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.content.decode()}")
        
        if response.status_code == 201:
            print("✓ 订单创建成功!")
        else:
            print("✗ 订单创建失败")
            
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == '__main__':
    test_order_creation()

