#!/usr/bin/env python
"""
初始化数据脚本
"""
import os
import sys
import django

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from apps.products.models import Category, Product
from apps.coupons.models import Coupon
from apps.delivery.models import DeliveryPerson

User = get_user_model()


def create_categories():
    """创建商品分类"""
    categories_data = [
        {
            'name': '桶装水',
            'description': '5100天然冰川矿泉水桶装水',
            'icon': 'https://example.com/icons/bucket.png',
            'sort_order': 1
        },
        {
            'name': '瓶装水',
            'description': '5100天然冰川矿泉水瓶装水',
            'icon': 'https://example.com/icons/bottle.png',
            'sort_order': 2
        },
        {
            'name': '家庭装',
            'description': '适合家庭使用的大容量装',
            'icon': 'https://example.com/icons/family.png',
            'sort_order': 3
        }
    ]
    
    for data in categories_data:
        category, created = Category.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        if created:
            print(f"创建分类: {category.name}")
        else:
            print(f"分类已存在: {category.name}")


def create_products():
    """创建商品"""
    try:
        bucket_category = Category.objects.get(name='桶装水')
        bottle_category = Category.objects.get(name='瓶装水')
    except Category.DoesNotExist:
        print("请先创建分类")
        return
    
    products_data = [
        {
            'name': '5100天然冰川矿泉水 18.9L桶装水',
            'description': '源自西藏念青唐古拉山脉，天然冰川矿泉水，富含多种矿物质',
            'category': bucket_category,
            'sku': '5100-BUCKET-18.9L',
            'price': 25.00,
            'original_price': 30.00,
            'stock': 100,
            'weight': 18.9,
            'volume': 18.9,
            'images': [
                'https://example.com/images/5100-bucket-18.9l-1.jpg',
                'https://example.com/images/5100-bucket-18.9l-2.jpg'
            ],
            'specifications': {
                '容量': '18.9L',
                '水源': '西藏念青唐古拉山脉',
                '保质期': '24个月',
                '包装': '食品级PC桶'
            },
            'is_featured': True,
            'sort_order': 1
        },
        {
            'name': '5100天然冰川矿泉水 500ml瓶装水',
            'description': '便携装天然冰川矿泉水，适合日常饮用',
            'category': bottle_category,
            'sku': '5100-BOTTLE-500ML',
            'price': 3.50,
            'original_price': 4.00,
            'stock': 500,
            'weight': 0.5,
            'volume': 0.5,
            'images': [
                'https://example.com/images/5100-bottle-500ml-1.jpg',
                'https://example.com/images/5100-bottle-500ml-2.jpg'
            ],
            'specifications': {
                '容量': '500ml',
                '水源': '西藏念青唐古拉山脉',
                '保质期': '24个月',
                '包装': '食品级PET瓶'
            },
            'is_featured': True,
            'sort_order': 2
        },
        {
            'name': '5100天然冰川矿泉水 1L瓶装水',
            'description': '家庭装天然冰川矿泉水，经济实惠',
            'category': bottle_category,
            'sku': '5100-BOTTLE-1L',
            'price': 5.00,
            'original_price': 6.00,
            'stock': 300,
            'weight': 1.0,
            'volume': 1.0,
            'images': [
                'https://example.com/images/5100-bottle-1l-1.jpg',
                'https://example.com/images/5100-bottle-1l-2.jpg'
            ],
            'specifications': {
                '容量': '1L',
                '水源': '西藏念青唐古拉山脉',
                '保质期': '24个月',
                '包装': '食品级PET瓶'
            },
            'is_featured': False,
            'sort_order': 3
        }
    ]
    
    for data in products_data:
        product, created = Product.objects.get_or_create(
            sku=data['sku'],
            defaults=data
        )
        if created:
            print(f"创建商品: {product.name}")
        else:
            print(f"商品已存在: {product.name}")


def create_coupons():
    """创建优惠券"""
    from django.utils import timezone
    from datetime import timedelta
    
    coupons_data = [
        {
            'name': '新用户专享券',
            'description': '新用户首次购买专享优惠',
            'coupon_type': 'cash',
            'discount_value': 5.00,
            'min_amount': 20.00,
            'total_count': 1000,
            'per_user_limit': 1,
            'valid_from': timezone.now(),
            'valid_to': timezone.now() + timedelta(days=30),
            'is_active': True
        },
        {
            'name': '满减券',
            'description': '满50减10元',
            'coupon_type': 'cash',
            'discount_value': 10.00,
            'min_amount': 50.00,
            'total_count': 500,
            'per_user_limit': 2,
            'valid_from': timezone.now(),
            'valid_to': timezone.now() + timedelta(days=15),
            'is_active': True
        },
        {
            'name': '折扣券',
            'description': '全场9折优惠',
            'coupon_type': 'discount',
            'discount_rate': 10.00,
            'min_amount': 30.00,
            'max_discount': 20.00,
            'total_count': 200,
            'per_user_limit': 1,
            'valid_from': timezone.now(),
            'valid_to': timezone.now() + timedelta(days=7),
            'is_active': True
        },
        {
            'name': '免运费券',
            'description': '免配送费',
            'coupon_type': 'free_shipping',
            'discount_value': 0.00,
            'min_amount': 0.00,
            'total_count': 1000,
            'per_user_limit': 3,
            'valid_from': timezone.now(),
            'valid_to': timezone.now() + timedelta(days=60),
            'is_active': True
        }
    ]
    
    for data in coupons_data:
        coupon, created = Coupon.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        if created:
            print(f"创建优惠券: {coupon.name}")
        else:
            print(f"优惠券已存在: {coupon.name}")


def create_delivery_persons():
    """创建配送员"""
    delivery_persons_data = [
        {
            'name': '张三',
            'phone': '13800138001',
            'id_card': '110101199001011234',
            'status': 1,
            'is_active': True
        },
        {
            'name': '李四',
            'phone': '13800138002',
            'id_card': '110101199002021234',
            'status': 1,
            'is_active': True
        },
        {
            'name': '王五',
            'phone': '13800138003',
            'id_card': '110101199003031234',
            'status': 0,
            'is_active': True
        }
    ]
    
    for data in delivery_persons_data:
        delivery_person, created = DeliveryPerson.objects.get_or_create(
            phone=data['phone'],
            defaults=data
        )
        if created:
            print(f"创建配送员: {delivery_person.name}")
        else:
            print(f"配送员已存在: {delivery_person.name}")


def create_admin_user():
    """创建管理员用户"""
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'nickname': '管理员',
            'phone': '13800138888',
            'is_staff': True,
            'is_superuser': True,
            'password': 'pbkdf2_sha256$260000$dummy$dummy'  # 需要设置真实密码
        }
    )
    
    if created:
        print("创建管理员用户: admin")
    else:
        print("管理员用户已存在: admin")


def main():
    """主函数"""
    print("开始初始化数据...")
    
    try:
        create_categories()
        create_products()
        create_coupons()
        create_delivery_persons()
        create_admin_user()
        
        print("数据初始化完成！")
    except Exception as e:
        print(f"初始化失败: {e}")


if __name__ == '__main__':
    main()
