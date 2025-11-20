#!/usr/bin/env python
"""
修复数据库迁移问题
"""
import os
import sys
import django
from django.conf import settings
from django.db import connection

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

def fix_migration():
    """修复迁移问题"""
    with connection.cursor() as cursor:
        try:
            # 检查字段是否已存在
            cursor.execute("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'products_productimage' 
                AND COLUMN_NAME = 'image_file'
            """)
            
            if cursor.fetchone():
                print("字段 image_file 已存在")
                return
            
            # 添加字段
            cursor.execute("""
                ALTER TABLE products_productimage 
                ADD COLUMN image_file VARCHAR(100) NULL COMMENT '图片文件路径'
            """)
            print("成功添加 image_file 字段")
            
            # 检查迁移记录
            cursor.execute("""
                SELECT * FROM django_migrations 
                WHERE app = 'products' AND name = '0003_productimage_image_file'
            """)
            
            if not cursor.fetchone():
                # 添加迁移记录
                cursor.execute("""
                    INSERT INTO django_migrations (app, name, applied) 
                    VALUES ('products', '0003_productimage_image_file', NOW())
                """)
                print("成功添加迁移记录")
            else:
                print("迁移记录已存在")
                
        except Exception as e:
            print(f"错误: {e}")
            return False
    
    return True

if __name__ == "__main__":
    if fix_migration():
        print("迁移修复完成！")
    else:
        print("迁移修复失败！")
        sys.exit(1)
