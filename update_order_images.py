#!/usr/bin/env python
"""
更新现有订单的商品图片URL
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.orders.models import OrderItem
from apps.products.models import Product

def update_order_images():
    """更新订单商品图片"""
    print("开始更新订单商品图片...")
    
    # 获取所有没有图片的订单商品
    order_items = OrderItem.objects.filter(product_image__isnull=True) | OrderItem.objects.filter(product_image='')
    
    updated_count = 0
    
    for item in order_items:
        try:
            # 获取商品的主图URL
            product_image_url = ''
            if item.product.images.exists():
                primary_image = item.product.images.filter(is_primary=True).first()
                if primary_image:
                    product_image_url = primary_image.get_image_url()
                else:
                    # 如果没有主图，使用第一张图片
                    first_image = item.product.images.first()
                    if first_image:
                        product_image_url = first_image.get_image_url()
            
            # 更新订单商品的图片URL
            if product_image_url:
                item.product_image = product_image_url
                item.save()
                updated_count += 1
                print(f"更新订单商品 {item.id}: {item.product_name} -> {product_image_url}")
            else:
                print(f"商品 {item.product_name} 没有图片")
                
        except Exception as e:
            print(f"更新订单商品 {item.id} 失败: {e}")
    
    print(f"更新完成，共更新了 {updated_count} 个订单商品")

if __name__ == '__main__':
    update_order_images()
