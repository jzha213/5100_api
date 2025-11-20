import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.orders.models import OrderItem

def fix_order_images():
    print("开始更新订单商品图片...")
    
    # 首先检查所有商品是否有图片
    from apps.products.models import Product, ProductImage
    products = Product.objects.all()
    print(f"数据库中共有 {products.count()} 个商品")
    
    for product in products:
        images = ProductImage.objects.filter(product=product)
        print(f"商品 {product.name} (ID: {product.id}) 有 {images.count()} 张图片")
        for img in images:
            print(f"  - 图片ID: {img.id}, URL: {img.image_url}, 文件: {img.image_file}")
    
    # 获取所有没有图片的订单商品
    from django.db.models import Q
    order_items = OrderItem.objects.filter(Q(product_image__isnull=True) | Q(product_image=''))
    
    print(f"找到 {order_items.count()} 个需要更新的订单商品")
    
    updated_count = 0
    
    for item in order_items:
        try:
            # 获取商品的主图URL
            product_image_url = ''
            print(f"检查商品 {item.product_name} 的图片...")
            print(f"商品ID: {item.product.id}")
            
            # 直接获取商品的图片
            images = item.product.product_images.all()
            print(f"商品图片数量: {images.count()}")
            
            if images:
                for i, img in enumerate(images):
                    print(f"图片 {i}: {img}")
                    if hasattr(img, 'image_url'):
                        print(f"  - image_url: {img.image_url}")
                    if hasattr(img, 'image_file'):
                        print(f"  - image_file: {img.image_file}")
                    if hasattr(img, 'is_primary'):
                        print(f"  - is_primary: {img.is_primary}")
                
                # 查找主图
                primary_image = None
                for img in images:
                    if hasattr(img, 'is_primary') and img.is_primary:
                        primary_image = img
                        break
                
                if primary_image:
                    product_image_url = primary_image.get_image_url()
                    print(f"找到主图: {product_image_url}")
                else:
                    # 如果没有主图，使用第一张图片
                    if images:
                        first_image = images[0]
                        product_image_url = first_image.get_image_url()
                        print(f"使用第一张图片: {product_image_url}")
            else:
                print("商品没有图片")
            
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
    fix_order_images()
