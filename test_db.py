#!/usr/bin/env python
"""
简单的数据库连接测试脚本
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line

def test_database():
    """测试数据库连接"""
    print("正在测试数据库连接...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print("✅ 数据库连接成功！")
            
            # 检查数据库是否存在
            cursor.execute("SHOW DATABASES LIKE '5100water'")
            db_exists = cursor.fetchone()
            if db_exists:
                print("✅ 数据库 '5100water' 存在")
            else:
                print("❌ 数据库 '5100water' 不存在，正在创建...")
                cursor.execute("CREATE DATABASE IF NOT EXISTS 5100water CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                print("✅ 数据库 '5100water' 创建成功")
            
            return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        print("\n可能的解决方案：")
        print("1. 检查MySQL服务是否启动")
        print("2. 检查端口3307是否正确")
        print("3. 检查用户名和密码是否正确")
        print("4. 检查MySQL是否允许远程连接")
        return False

def run_migrations():
    """运行数据库迁移"""
    print("\n正在运行数据库迁移...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ 数据库迁移完成！")
        return True
    except Exception as e:
        print(f"❌ 数据库迁移失败: {e}")
        return False

def create_superuser():
    """创建超级用户"""
    print("\n正在创建超级用户...")
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@5100water.com',
                password='admin123'
            )
            print("✅ 创建超级用户: admin/admin123")
        else:
            print("✅ 超级用户已存在")
        return True
    except Exception as e:
        print(f"❌ 创建超级用户失败: {e}")
        return False

def main():
    print("=" * 60)
    print("5100天然冰川矿泉水订水系统 - 数据库测试")
    print("=" * 60)
    
    # 测试数据库连接
    if not test_database():
        return
    
    # 运行迁移
    if not run_migrations():
        return
    
    # 创建超级用户
    create_superuser()
    
    print("\n" + "=" * 60)
    print("数据库设置完成！")
    print("现在可以访问admin后台了")
    print("用户名: admin")
    print("密码: admin123")
    print("=" * 60)

if __name__ == '__main__':
    main()
