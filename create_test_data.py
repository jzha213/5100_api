#!/usr/bin/env python
"""
创建测试数据脚本
为5100订水系统创建示例数据
"""
import os
import django
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.products.models import Category, Product, ProductImage, ProductSpecification
from apps.users.models import User, UserProfile
from decimal import Decimal

def create_categories():
    """创建商品分类"""
    print("📦 创建商品分类...")
    
    categories_data = [
        {
            'name': '5100天然冰川矿泉水',
            'description': '来自西藏念青唐古拉山脉的天然冰川矿泉水',
            'sort_order': 1,
            'is_active': True
        },
        {
            'name': '瓶装水',
            'description': '各种规格的瓶装矿泉水',
            'sort_order': 2,
            'is_active': True
        },
        {
            'name': '桶装水',
            'description': '大容量桶装水，适合家庭和办公使用',
            'sort_order': 3,
            'is_active': True
        }
    ]
    
    created_categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        if created:
            print(f"  ✅ 创建分类: {category.name}")
        else:
            print(f"  ℹ️  分类已存在: {category.name}")
        created_categories.append(category)
    
    return created_categories

def create_products(categories):
    """创建商品"""
    print("\n💧 创建商品...")
    
    products_data = [
        {
            'name': '5100天然冰川矿泉水 330ml',
            'description': '来自西藏念青唐古拉山脉海拔5100米的天然冰川矿泉水，口感甘甜，富含多种矿物质',
            'category': categories[0],
            'sku': '5100-330ML',
            'price': Decimal('3.50'),
            'original_price': Decimal('4.00'),
            'stock': 1000,
            'is_active': True,
            'is_featured': True,
            'sort_order': 1,
            'weight': 0.35,
            'volume': 0.33,
            'specifications': {'origin': '西藏念青唐古拉山脉', 'altitude': '5100米'}
        },
        {
            'name': '5100天然冰川矿泉水 500ml',
            'description': '经典500ml装，适合日常饮用',
            'category': categories[0],
            'sku': '5100-500ML',
            'price': Decimal('4.50'),
            'original_price': Decimal('5.00'),
            'stock': 800,
            'is_active': True,
            'is_featured': True,
            'sort_order': 2,
            'weight': 0.52,
            'volume': 0.5,
            'specifications': {'origin': '西藏念青唐古拉山脉', 'altitude': '5100米'}
        },
        {
            'name': '5100天然冰川矿泉水 1.5L',
            'description': '家庭装1.5L大瓶装，经济实惠',
            'category': categories[0],
            'sku': '5100-1500ML',
            'price': Decimal('8.00'),
            'original_price': Decimal('9.00'),
            'stock': 500,
            'is_active': True,
            'is_featured': False,
            'sort_order': 3,
            'weight': 1.55,
            'volume': 1.5,
            'specifications': {'origin': '西藏念青唐古拉山脉', 'altitude': '5100米'}
        },
        {
            'name': '5100天然冰川矿泉水 19L桶装',
            'description': '大容量桶装水，适合家庭和办公使用，配有专用饮水机',
            'category': categories[2],
            'sku': '5100-19L',
            'price': Decimal('25.00'),
            'original_price': Decimal('30.00'),
            'stock': 200,
            'is_active': True,
            'is_featured': True,
            'sort_order': 4,
            'weight': 19.5,
            'volume': 19.0,
            'specifications': {'origin': '西藏念青唐古拉山脉', 'altitude': '5100米', 'delivery': '免费配送'}
        }
    ]
    
    created_products = []
    for prod_data in products_data:
        product, created = Product.objects.get_or_create(
            sku=prod_data['sku'],
            defaults=prod_data
        )
        if created:
            print(f"  ✅ 创建商品: {product.name} - ¥{product.price}")
        else:
            print(f"  ℹ️  商品已存在: {product.name}")
        created_products.append(product)
    
    return created_products

def create_product_specifications(products):
    """创建商品规格"""
    print("\n📋 创建商品规格...")
    
    specifications_data = [
        # 330ml规格
        {
            'product': products[0],
            'name': '水源',
            'value': '西藏念青唐古拉山脉海拔5100米冰川水',
            'sort_order': 1
        },
        {
            'product': products[0],
            'name': '矿物质含量',
            'value': '富含钙、镁、钾、钠等天然矿物质',
            'sort_order': 2
        },
        {
            'product': products[0],
            'name': 'pH值',
            'value': '7.3±0.5（弱碱性）',
            'sort_order': 3
        },
        # 500ml规格
        {
            'product': products[1],
            'name': '水源',
            'value': '西藏念青唐古拉山脉海拔5100米冰川水',
            'sort_order': 1
        },
        {
            'product': products[1],
            'name': '保质期',
            'value': '24个月',
            'sort_order': 2
        },
        # 1.5L规格
        {
            'product': products[2],
            'name': '水源',
            'value': '西藏念青唐古拉山脉海拔5100米冰川水',
            'sort_order': 1
        },
        {
            'product': products[2],
            'name': '包装',
            'value': '环保PET材质',
            'sort_order': 2
        },
        # 19L桶装规格
        {
            'product': products[3],
            'name': '水源',
            'value': '西藏念青唐古拉山脉海拔5100米冰川水',
            'sort_order': 1
        },
        {
            'product': products[3],
            'name': '配送',
            'value': '免费配送上门，空桶回收',
            'sort_order': 2
        },
        {
            'product': products[3],
            'name': '保质期',
            'value': '开封后建议7天内饮用完毕',
            'sort_order': 3
        }
    ]
    
    for spec_data in specifications_data:
        spec, created = ProductSpecification.objects.get_or_create(
            product=spec_data['product'],
            name=spec_data['name'],
            defaults=spec_data
        )
        if created:
            print(f"  ✅ 创建规格: {spec.product.name} - {spec.name}: {spec.value}")
        else:
            print(f"  ℹ️  规格已存在: {spec.product.name} - {spec.name}")

def create_test_users():
    """创建测试用户"""
    print("\n👤 创建测试用户...")
    
    users_data = [
        {
            'username': 'testuser1',
            'email': 'testuser1@example.com',
            'phone': '13800138001',
            'nickname': '测试用户1',
            'status': 1
        },
        {
            'username': 'testuser2',
            'email': 'testuser2@example.com',
            'phone': '13800138002',
            'nickname': '测试用户2',
            'status': 1
        }
    ]
    
    created_users = []
    for user_data in users_data:
        try:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'phone': user_data['phone'],
                    'nickname': user_data['nickname'],
                    'status': user_data['status']
                }
            )
            if created:
                user.set_password('test123456')  # 设置密码
                user.save()
                print(f"  ✅ 创建用户: {user.username} ({user.nickname})")
            else:
                print(f"  ℹ️  用户已存在: {user.username}")
            created_users.append(user)
        except Exception as e:
            print(f"  ❌ 创建用户失败: {user_data['username']} - {e}")
            continue
    
    return created_users

def main():
    """主函数"""
    print("🚀 开始创建5100订水系统测试数据...")
    print("=" * 60)
    
    try:
        # 创建分类
        categories = create_categories()
        
        # 创建商品
        products = create_products(categories)
        
        # 创建商品规格
        create_product_specifications(products)
        
        # 创建测试用户
        users = create_test_users()
        
        print("\n" + "=" * 60)
        print("🎉 测试数据创建完成！")
        print(f"📊 统计信息:")
        print(f"  - 分类: {Category.objects.count()} 个")
        print(f"  - 商品: {Product.objects.count()} 个")
        print(f"  - 规格: {ProductSpecification.objects.count()} 个")
        print(f"  - 用户: {User.objects.count()} 个")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 创建测试数据时出错: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ 测试数据创建成功！")
    else:
        print("\n❌ 测试数据创建失败！")
