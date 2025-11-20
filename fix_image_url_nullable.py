import os
import django
from django.conf import settings
import pymysql

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

def fix_image_url_nullable():
    """修复 image_url 字段允许为空的问题"""
    db_settings = settings.DATABASES['default']
    
    try:
        # 连接到数据库
        conn = pymysql.connect(
            host=db_settings['HOST'],
            port=int(db_settings['PORT']),  # 确保端口是整数
            user=db_settings['USER'],
            password=db_settings['PASSWORD'],
            database=db_settings['NAME'],
            charset=db_settings['OPTIONS'].get('charset', 'utf8mb4')
        )
        cursor = conn.cursor()

        # 1. 检查当前字段结构
        cursor.execute("DESCRIBE products_productimage")
        columns = cursor.fetchall()
        print("当前 products_productimage 表结构:")
        for col in columns:
            print(f"  {col[0]}: {col[1]} {col[2]} {col[3]} {col[4]}")
        
        # 2. 修改 image_url 字段允许为空
        print("\n正在修改 image_url 字段...")
        cursor.execute("ALTER TABLE products_productimage MODIFY COLUMN image_url VARCHAR(200) NULL")
        conn.commit()
        print("✅ 成功修改 image_url 字段允许为空")

        # 3. 验证修改结果
        cursor.execute("DESCRIBE products_productimage")
        columns = cursor.fetchall()
        print("\n修改后的 products_productimage 表结构:")
        for col in columns:
            if col[0] == 'image_url':
                print(f"  {col[0]}: {col[1]} {col[2]} {col[3]} {col[4]} ← 已修改")
            else:
                print(f"  {col[0]}: {col[1]} {col[2]} {col[3]} {col[4]}")

        print("\n🎉 修复完成！现在可以在Django后台添加商品图片了。")

    except Exception as e:
        print(f"❌ 修复过程中发生错误: {e}")
    finally:
        if 'conn' in locals() and conn.open:
            conn.close()

if __name__ == '__main__':
    fix_image_url_nullable()
