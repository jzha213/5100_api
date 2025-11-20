#!/usr/bin/env python
"""
检查数据库连接和创建测试数据的脚本
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line
from apps.users.models import User
from apps.products.models import Product, Category
from apps.orders.models import Order, OrderItem
from apps.addresses.models import Address
from apps.coupons.models import Coupon

def check_database_connection():
    """检查数据库连接"""
    print("正在检查数据库连接...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print("✅ 数据库连接成功！")
            return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

def run_migrations():
    """运行数据库迁移"""
    print("正在运行数据库迁移...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ 数据库迁移完成！")
        return True
    except Exception as e:
        print(f"❌ 数据库迁移失败: {e}")
        return False

def create_test_data():
    """创建测试数据"""
    print("正在创建测试数据...")
    
    try:
        # 创建超级用户
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@5100water.com',
                password='admin123'
            )
            print("✅ 创建超级用户: admin/admin123")
        
        # 创建测试用户
        if not User.objects.filter(username='testuser').exists():
            User.objects.create_user(
                username='testuser',
                email='test@5100water.com',
                password='test123',
                phone='13800138000'
            )
            print("✅ 创建测试用户: testuser/test123")
        
        # 创建产品分类
        category, created = Category.objects.get_or_create(
            name='天然矿泉水',
            defaults={'description': '5100天然冰川矿泉水'}
        )
        if created:
            print("✅ 创建产品分类: 天然矿泉水")
        
        # 创建测试产品
        if not Product.objects.exists():
            products = [
                {
                    'name': '5100天然冰川矿泉水 330ml',
                    'description': '来自西藏念青唐古拉山脉的天然矿泉水',
                    'price': 3.50,
                    'stock': 1000,
                    'category': category
                },
                {
                    'name': '5100天然冰川矿泉水 500ml',
                    'description': '来自西藏念青唐古拉山脉的天然矿泉水',
                    'price': 5.00,
                    'stock': 800,
                    'category': category
                },
                {
                    'name': '5100天然冰川矿泉水 1L',
                    'description': '来自西藏念青唐古拉山脉的天然矿泉水',
                    'price': 8.50,
                    'stock': 600,
                    'category': category
                }
            ]
            
            for product_data in products:
                Product.objects.create(**product_data)
            print("✅ 创建测试产品")
        
        # 创建优惠券
        if not Coupon.objects.exists():
            Coupon.objects.create(
                name='新用户优惠券',
                code='NEWUSER10',
                discount_type='percentage',
                discount_value=10,
                min_order_amount=50.00,
                max_discount=20.00,
                usage_limit=100,
                is_active=True
            )
            print("✅ 创建测试优惠券")
        
        print("✅ 测试数据创建完成！")
        return True
        
    except Exception as e:
        print(f"❌ 创建测试数据失败: {e}")
        return False

def main():
    print("=" * 50)
    print("数据库检查和测试数据创建脚本")
    print("=" * 50)
    
    # 检查数据库连接
    if not check_database_connection():
        print("\n请检查MySQL服务是否启动，端口是否为3307")
        return
    
    # 运行迁移
    if not run_migrations():
        print("\n数据库迁移失败，请检查数据库配置")
        return
    
    # 创建测试数据
    create_test_data()
    
    print("\n" + "=" * 50)
    print("数据库设置完成！")
    print("现在可以访问admin后台查看测试数据了")
    print("=" * 50)

if __name__ == '__main__':
    main()
