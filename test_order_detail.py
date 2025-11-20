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
from apps.orders.models import Order

User = get_user_model()

def test_order_detail():
    """测试订单详情API"""
    client = Client()
    
    try:
        # 获取admin用户
        user = User.objects.get(username='admin')
        print(f"找到用户: {user.username}")
        
        # 获取用户的第一个订单
        order = Order.objects.filter(user=user).first()
        if not order:
            print("用户没有订单")
            return
            
        print(f"找到订单: {order.id}")
        
        # 创建JWT token
        token = AccessToken.for_user(user)
        
        # 设置认证头
        headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        
        # 发送GET请求
        response = client.get(f'/api/v1/orders/{order.id}/', **headers)
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            import json
            data = json.loads(response.content.decode())
            print("订单详情数据:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # 检查商品信息
            if 'items' in data and data['items']:
                print(f"\n商品数量: {len(data['items'])}")
                for item in data['items']:
                    print(f"商品: {item.get('product_name', 'N/A')}")
                    print(f"价格: {item.get('price', 'N/A')}")
                    print(f"数量: {item.get('quantity', 'N/A')}")
                    print(f"小计: {item.get('subtotal', 'N/A')}")
            else:
                print("没有商品信息")
        else:
            print(f"请求失败: {response.content.decode()}")
            
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == '__main__':
    test_order_detail()

