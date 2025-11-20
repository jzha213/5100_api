#!/usr/bin/env python
"""
Admin后台数据调试脚本
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.db import connection
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import site
from django.apps import apps

def check_database_connection():
    """检查数据库连接"""
    print("=" * 60)
    print("1. 检查数据库连接")
    print("=" * 60)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print("✅ Django数据库连接成功")
            
            # 检查当前数据库
            cursor.execute("SELECT DATABASE()")
            current_db = cursor.fetchone()[0]
            print(f"✅ 当前数据库: {current_db}")
            
            # 检查表
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"✅ 数据库中有 {len(tables)} 个表:")
            for table in tables:
                print(f"  - {table[0]}")
                
                # 检查每个表的记录数
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                    count = cursor.fetchone()[0]
                    print(f"    记录数: {count}")
                except Exception as e:
                    print(f"    无法获取记录数: {e}")
            
            return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

def check_models():
    """检查模型"""
    print("\n" + "=" * 60)
    print("2. 检查Django模型")
    print("=" * 60)
    
    try:
        models = apps.get_models()
        print(f"✅ 找到 {len(models)} 个模型:")
        
        for model in models:
            print(f"\n📋 模型: {model.__name__}")
            print(f"   应用: {model._meta.app_label}")
            print(f"   表名: {model._meta.db_table}")
            
            try:
                count = model.objects.count()
                print(f"   记录数: {count}")
                
                if count > 0:
                    # 显示前几条记录
                    objects = model.objects.all()[:3]
                    for obj in objects:
                        print(f"   - {obj}")
                        
            except Exception as e:
                print(f"   ❌ 错误: {e}")
                
    except Exception as e:
        print(f"❌ 检查模型失败: {e}")

def check_admin_registration():
    """检查admin注册"""
    print("\n" + "=" * 60)
    print("3. 检查Admin注册")
    print("=" * 60)
    
    try:
        registered_models = []
        for model, admin_class in site._registry.items():
            registered_models.append({
                'model': model,
                'admin_class': admin_class,
                'app_label': model._meta.app_label,
                'model_name': model._meta.model_name
            })
        
        print(f"✅ 已注册 {len(registered_models)} 个模型到admin:")
        
        for item in registered_models:
            model = item['model']
            print(f"\n📋 {item['app_label']}.{item['model_name']}")
            print(f"   Admin类: {item['admin_class'].__class__.__name__}")
            
            try:
                count = model.objects.count()
                print(f"   记录数: {count}")
            except Exception as e:
                print(f"   ❌ 错误: {e}")
                
    except Exception as e:
        print(f"❌ 检查admin注册失败: {e}")

def create_test_data():
    """创建测试数据"""
    print("\n" + "=" * 60)
    print("4. 创建测试数据")
    print("=" * 60)
    
    try:
        User = get_user_model()
        
        # 创建超级用户
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@5100water.com',
                password='admin123'
            )
            print("✅ 创建超级用户: admin/admin123")
        else:
            print("✅ 超级用户已存在")
        
        # 创建测试用户
        if not User.objects.filter(username='testuser').exists():
            User.objects.create_user(
                username='testuser',
                email='test@5100water.com',
                password='test123',
                phone='13800138000'
            )
            print("✅ 创建测试用户: testuser/test123")
        
        # 尝试创建其他模型的数据
        try:
            from apps.products.models import Product, Category
            
            # 创建分类
            category, created = Category.objects.get_or_create(
                name='天然矿泉水',
                defaults={'description': '5100天然冰川矿泉水'}
            )
            if created:
                print("✅ 创建产品分类")
            
            # 创建产品
            if not Product.objects.exists():
                Product.objects.create(
                    name='5100天然冰川矿泉水 330ml',
                    description='来自西藏念青唐古拉山脉的天然矿泉水',
                    price=3.50,
                    stock=1000,
                    category=category
                )
                print("✅ 创建测试产品")
                
        except Exception as e:
            print(f"❌ 创建产品数据失败: {e}")
            
        # 尝试创建订单数据
        try:
            from apps.orders.models import Order, OrderItem
            
            if not Order.objects.exists():
                user = User.objects.first()
                order = Order.objects.create(
                    user=user,
                    total_amount=10.50,
                    status='pending'
                )
                print("✅ 创建测试订单")
                
        except Exception as e:
            print(f"❌ 创建订单数据失败: {e}")
            
    except Exception as e:
        print(f"❌ 创建测试数据失败: {e}")

def check_admin_urls():
    """检查admin URL配置"""
    print("\n" + "=" * 60)
    print("5. 检查Admin URL配置")
    print("=" * 60)
    
    try:
        from django.urls import reverse
        from django.contrib.admin.sites import site
        
        print("✅ Admin URL配置:")
        print(f"   Admin根URL: {reverse('admin:index')}")
        
        # 检查各个应用的admin URL
        for model, admin_class in site._registry.items():
            try:
                url_name = f"admin:{model._meta.app_label}_{model._meta.model_name}_changelist"
                url = reverse(url_name)
                print(f"   {model._meta.app_label}.{model._meta.model_name}: {url}")
            except Exception as e:
                print(f"   ❌ {model._meta.app_label}.{model._meta.model_name}: {e}")
                
    except Exception as e:
        print(f"❌ 检查admin URL失败: {e}")

def main():
    print("=" * 70)
    print("Admin后台数据调试脚本")
    print("=" * 70)
    
    # 1. 检查数据库连接
    if not check_database_connection():
        print("\n❌ 数据库连接失败，请检查MySQL配置")
        return
    
    # 2. 检查模型
    check_models()
    
    # 3. 检查admin注册
    check_admin_registration()
    
    # 4. 创建测试数据
    create_test_data()
    
    # 5. 检查admin URL
    check_admin_urls()
    
    print("\n" + "=" * 70)
    print("调试完成！")
    print("如果admin后台仍然没有数据，请检查：")
    print("1. 浏览器缓存 - 按Ctrl+F5强制刷新")
    print("2. Django模板是否正确加载")
    print("3. 静态文件是否正确收集")
    print("=" * 70)

if __name__ == '__main__':
    main()
