#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from apps.users.models import User
from apps.addresses.models import Address

def create_test_address():
    """为admin用户创建测试地址"""
    try:
        # 获取admin用户
        user = User.objects.get(username='admin')
        print(f"找到用户: {user.username}")
        
        # 检查是否已有地址
        existing_address = Address.objects.filter(user=user).first()
        if existing_address:
            print(f"用户已有地址: {existing_address}")
            return existing_address.id
        
        # 创建测试地址
        address = Address.objects.create(
            user=user,
            name='测试收货人',
            phone='13800138000',
            province='北京市',
            city='北京市',
            district='朝阳区',
            street='三里屯街道',
            detail_address='三里屯SOHO A座1001室',
            is_default=True
        )
        
        print(f"创建测试地址成功: {address}")
        print(f"地址ID: {address.id}")
        return address.id
        
    except User.DoesNotExist:
        print("未找到admin用户，请先创建用户")
        return None
    except Exception as e:
        print(f"创建地址失败: {e}")
        return None

if __name__ == '__main__':
    address_id = create_test_address()
    if address_id:
        print(f"\n测试地址ID: {address_id}")
        print("现在可以测试订单创建了")
    else:
        print("创建地址失败")

