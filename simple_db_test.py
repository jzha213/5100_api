#!/usr/bin/env python
"""
简单的数据库测试脚本
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from django.core.management import execute_from_command_line

def main():
    print("=" * 50)
    print("简单数据库测试")
    print("=" * 50)
    
    try:
        # 创建超级用户
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
        
        # 创建测试用户
        if not User.objects.filter(username='testuser').exists():
            User.objects.create_user(
                username='testuser',
                email='test@5100water.com',
                password='test123'
            )
            print("✅ 创建测试用户: testuser/test123")
        
        # 显示用户数量
        user_count = User.objects.count()
        print(f"✅ 总用户数: {user_count}")
        
        print("\n" + "=" * 50)
        print("数据库测试完成！")
        print("现在可以访问admin后台查看用户数据了")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ 数据库测试失败: {e}")

if __name__ == '__main__':
    main()
