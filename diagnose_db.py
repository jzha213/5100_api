#!/usr/bin/env python
"""
数据库连接诊断脚本
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

import pymysql
from django.db import connection
from django.core.management import execute_from_command_line

def test_mysql_connection():
    """直接测试MySQL连接"""
    print("正在测试MySQL连接...")
    try:
        # 尝试连接MySQL
        connection_mysql = pymysql.connect(
            host='127.0.0.1',
            port=3307,
            user='root',
            password='zjzj828',
            charset='utf8mb4'
        )
        
        cursor = connection_mysql.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"✅ MySQL连接成功！版本: {version[0]}")
        
        # 检查数据库是否存在
        cursor.execute("SHOW DATABASES LIKE '5100water'")
        db_exists = cursor.fetchone()
        
        if db_exists:
            print("✅ 数据库 '5100water' 存在")
            
            # 连接到5100water数据库
            cursor.execute("USE 5100water")
            
            # 查看数据库中的表
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if tables:
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
            else:
                print("❌ 数据库中没有表")
                
        else:
            print("❌ 数据库 '5100water' 不存在")
            print("正在创建数据库...")
            cursor.execute("CREATE DATABASE 5100water CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("✅ 数据库 '5100water' 创建成功")
        
        connection_mysql.close()
        return True
        
    except Exception as e:
        print(f"❌ MySQL连接失败: {e}")
        print("\n可能的解决方案：")
        print("1. 检查MySQL服务是否启动")
        print("2. 检查端口3307是否正确")
        print("3. 检查防火墙设置")
        print("4. 尝试使用其他端口（如3306）")
        return False

def test_django_db_connection():
    """测试Django数据库连接"""
    print("\n正在测试Django数据库连接...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print("✅ Django数据库连接成功！")
            return True
    except Exception as e:
        print(f"❌ Django数据库连接失败: {e}")
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

def create_test_data():
    """创建测试数据"""
    print("\n正在创建测试数据...")
    try:
        from django.contrib.auth import get_user_model
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
        
        # 检查是否有其他模型的数据
        try:
            from apps.products.models import Product
            if Product.objects.exists():
                print(f"✅ 产品数据: {Product.objects.count()} 条")
            else:
                print("❌ 没有产品数据")
        except Exception as e:
            print(f"产品模型错误: {e}")
            
        return True
        
    except Exception as e:
        print(f"❌ 创建测试数据失败: {e}")
        return False

def check_models():
    """检查模型定义"""
    print("\n正在检查模型定义...")
    try:
        from django.apps import apps
        models = apps.get_models()
        print(f"✅ 找到 {len(models)} 个模型:")
        for model in models:
            print(f"  - {model.__name__}")
            try:
                count = model.objects.count()
                print(f"    记录数: {count}")
            except Exception as e:
                print(f"    错误: {e}")
    except Exception as e:
        print(f"❌ 检查模型失败: {e}")

def main():
    print("=" * 70)
    print("5100天然冰川矿泉水订水系统 - 数据库诊断")
    print("=" * 70)
    
    # 1. 测试MySQL连接
    if not test_mysql_connection():
        return
    
    # 2. 测试Django数据库连接
    if not test_django_db_connection():
        return
    
    # 3. 运行迁移
    if not run_migrations():
        return
    
    # 4. 检查模型
    check_models()
    
    # 5. 创建测试数据
    create_test_data()
    
    print("\n" + "=" * 70)
    print("数据库诊断完成！")
    print("现在可以访问admin后台查看数据了")
    print("用户名: admin")
    print("密码: admin123")
    print("=" * 70)

if __name__ == '__main__':
    main()
