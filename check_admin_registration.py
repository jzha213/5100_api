#!/usr/bin/env python
"""
检查admin注册情况
"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib import admin
from django.apps import apps

def check_admin_registration():
    """检查admin注册情况"""
    print("🔍 检查Django Admin注册情况...")
    print("=" * 50)
    
    # 获取所有已注册的模型
    registered_models = admin.site._registry.keys()
    print(f"已注册的模型数量: {len(registered_models)}")
    
    print("\n📋 已注册的模型:")
    for model in registered_models:
        app_label = model._meta.app_label
        model_name = model._meta.model_name
        verbose_name = model._meta.verbose_name
        print(f"   - {app_label}.{model_name} ({verbose_name})")
    
    # 检查我们的自定义应用
    print("\n🔍 检查自定义应用:")
    our_apps = ['users', 'products', 'orders', 'addresses', 'coupons']
    
    for app_name in our_apps:
        try:
            app_config = apps.get_app_config(app_name)
            models = app_config.get_models()
            print(f"\n📱 {app_name} 应用:")
            print(f"   模型数量: {len(models)}")
            
            for model in models:
                model_name = model._meta.model_name
                verbose_name = model._meta.verbose_name
                is_registered = model in registered_models
                status = "✅" if is_registered else "❌"
                print(f"   {status} {model_name} ({verbose_name}) - {'已注册' if is_registered else '未注册'}")
                
        except Exception as e:
            print(f"   ❌ 无法获取 {app_name} 应用: {e}")
    
    # 检查admin.py文件是否存在
    print("\n🔍 检查admin.py文件:")
    for app_name in our_apps:
        admin_file = f"apps/{app_name}/admin.py"
        if os.path.exists(admin_file):
            print(f"   ✅ {admin_file} 存在")
        else:
            print(f"   ❌ {admin_file} 不存在")

def test_import_admin():
    """测试导入admin模块"""
    print("\n🔍 测试导入admin模块...")
    
    admin_modules = [
        'apps.users.admin',
        'apps.products.admin', 
        'apps.orders.admin',
        'apps.addresses.admin',
        'apps.coupons.admin'
    ]
    
    for module in admin_modules:
        try:
            __import__(module)
            print(f"   ✅ {module} 导入成功")
        except Exception as e:
            print(f"   ❌ {module} 导入失败: {e}")

if __name__ == "__main__":
    check_admin_registration()
    test_import_admin()
