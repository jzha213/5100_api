#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.urls import reverse
from django.test import Client

def test_urls():
    """测试URL配置"""
    client = Client()
    
    # 测试订单创建URL
    try:
        response = client.post('/api/v1/orders/create/', {
            'items': [{'product_id': 1, 'quantity': 1}]
        })
        print(f"订单创建URL测试: {response.status_code}")
        if response.status_code == 401:
            print("✓ URL配置正确，需要认证")
        elif response.status_code == 400:
            print("✓ URL配置正确，数据验证失败")
        else:
            print(f"响应内容: {response.content.decode()[:200]}")
    except Exception as e:
        print(f"订单创建URL测试失败: {e}")
    
    # 测试购物车URL
    try:
        response = client.get('/api/v1/cart/')
        print(f"购物车URL测试: {response.status_code}")
        if response.status_code == 401:
            print("✓ 购物车URL配置正确，需要认证")
        else:
            print(f"响应内容: {response.content.decode()[:200]}")
    except Exception as e:
        print(f"购物车URL测试失败: {e}")

if __name__ == '__main__':
    test_urls()

