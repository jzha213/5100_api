from rest_framework import serializers
from .models import Order, OrderItem, Cart, OrderStatusLog


class OrderItemSerializer(serializers.ModelSerializer):
    """订单商品序列化器"""
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_name', 'product_image', 'product_sku',
            'price', 'quantity', 'subtotal'
        ]


class OrderStatusLogSerializer(serializers.ModelSerializer):
    """订单状态日志序列化器"""
    operator_name = serializers.CharField(source='operator.nickname', read_only=True)
    
    class Meta:
        model = OrderStatusLog
        fields = ['from_status', 'to_status', 'operator_name', 'remark', 'created_at']


class OrderListSerializer(serializers.ModelSerializer):
    """订单列表序列化器"""
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_no', 'status', 'status_display', 'payment_status', 
            'payment_status_display', 'total_amount', 'final_amount', 
            'payment_method', 'items', 'created_at'
        ]


class OrderDetailSerializer(serializers.ModelSerializer):
    """订单详情序列化器"""
    items = OrderItemSerializer(many=True, read_only=True)
    status_logs = OrderStatusLogSerializer(many=True, read_only=True)
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    user_phone = serializers.CharField(source='user.phone', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    
    # 地址信息
    delivery_address = serializers.SerializerMethodField()
    contact_name = serializers.SerializerMethodField()
    contact_phone = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_no', 'status', 'status_display', 'payment_status', 
            'payment_status_display', 'payment_method', 'payment_method_display',
            'total_amount', 'discount_amount', 'shipping_fee', 'final_amount',
            'payment_time', 'delivery_time', 'completed_time', 'cancel_reason', 
            'remark', 'user_nickname', 'user_phone', 'items', 'status_logs',
            'delivery_address', 'contact_name', 'contact_phone', 'address',
            'created_at', 'updated_at'
        ]
    
    def get_delivery_address(self, obj):
        """获取配送地址"""
        try:
            delivery = obj.delivery
            return delivery.delivery_address
        except:
            return None
    
    def get_contact_name(self, obj):
        """获取联系人姓名"""
        try:
            delivery = obj.delivery
            return delivery.contact_name
        except:
            return None
    
    def get_contact_phone(self, obj):
        """获取联系人电话"""
        try:
            delivery = obj.delivery
            return delivery.contact_phone
        except:
            return None
    
    def get_address(self, obj):
        """获取详细地址信息"""
        try:
            delivery = obj.delivery
            return {
                'name': delivery.contact_name,
                'phone': delivery.contact_phone,
                'province': getattr(delivery, 'province', ''),
                'city': getattr(delivery, 'city', ''),
                'district': getattr(delivery, 'district', ''),
                'street': getattr(delivery, 'street', ''),
                'detail_address': getattr(delivery, 'detail_address', ''),
                'is_default': True
            }
        except:
            return None


class OrderCreateSerializer(serializers.ModelSerializer):
    """订单创建序列化器"""
    items = serializers.ListField(write_only=True)
    address_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Order
        fields = ['address_id', 'items', 'remark']
    
    def validate_address_id(self, value):
        """验证地址ID"""
        # 暂时跳过地址验证，允许使用默认地址ID
        if not isinstance(value, int):
            raise serializers.ValidationError("地址ID必须是整数")
        return value
    
    def validate_items(self, value):
        """验证订单商品"""
        if not value:
            raise serializers.ValidationError("订单商品不能为空")
        
        for item in value:
            if 'product_id' not in item or 'quantity' not in item:
                raise serializers.ValidationError("订单商品信息不完整")
            
            # 检查product_id和quantity是否为None
            if item['product_id'] is None:
                raise serializers.ValidationError("商品ID不能为空")
            
            if item['quantity'] is None:
                raise serializers.ValidationError("商品数量不能为空")
            
            if item['quantity'] <= 0:
                raise serializers.ValidationError("商品数量必须大于0")
        
        return value
    
    def create(self, validated_data):
        user = self.context['request'].user
        items_data = validated_data.pop('items')
        address_id = validated_data.pop('address_id')
        
        # 获取用户选择的地址
        try:
            from apps.addresses.models import Address
            address = Address.objects.get(id=address_id, user=user)
            address_info = {
                'name': address.name,
                'phone': address.phone,
                'province': address.province,
                'city': address.city,
                'district': address.district,
                'street': address.street,
                'detail_address': address.detail_address
            }
        except Address.DoesNotExist:
            raise serializers.ValidationError(f"地址ID {address_id} 不存在或不属于当前用户")
        
        # 计算订单金额
        total_amount = 0
        order_items = []
        
        for item_data in items_data:
            from apps.products.models import Product
            try:
                product = Product.objects.get(id=item_data['product_id'])
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"商品ID {item_data['product_id']} 不存在")
            
            if product.stock < item_data['quantity']:
                raise serializers.ValidationError(f"商品 {product.name} 库存不足")
            
            subtotal = product.price * item_data['quantity']
            total_amount += subtotal
            
            # 获取商品主图URL
            product_image_url = ''
            # 使用正确的关联名称获取图片
            images = product.product_images.all()
            if images.exists():
                primary_image = images.filter(is_primary=True).first()
                if primary_image:
                    product_image_url = primary_image.get_image_url()
                else:
                    # 如果没有主图，使用第一张图片
                    first_image = images.first()
                    if first_image:
                        product_image_url = first_image.get_image_url()
            
            order_items.append({
                'product': product,
                'product_name': product.name,
                'product_image': product_image_url,
                'product_sku': product.sku,
                'price': product.price,
                'quantity': item_data['quantity'],
                'subtotal': subtotal
            })
        
        # 创建订单
        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            final_amount=total_amount,  # 暂时不考虑优惠和运费
            **validated_data
        )
        
        # 创建订单商品
        for item_data in order_items:
            OrderItem.objects.create(order=order, **item_data)
        
        # 创建配送记录
        from apps.delivery.models import Delivery
        Delivery.objects.create(
            order=order,
            delivery_address=f"{address_info['province']}{address_info['city']}{address_info['district']}{address_info['street']}{address_info['detail_address']}",
            contact_name=address_info['name'],
            contact_phone=address_info['phone'],
            # 保存完整的地址信息到配送记录
            province=address_info['province'],
            city=address_info['city'],
            district=address_info['district'],
            street=address_info['street'],
            detail_address=address_info['detail_address']
        )
        
        return order


class OrderUpdateSerializer(serializers.ModelSerializer):
    """订单更新序列化器"""
    
    class Meta:
        model = Order
        fields = ['status', 'payment_status', 'payment_time', 'delivery_time', 'completed_time', 'cancel_reason']


class CartSerializer(serializers.ModelSerializer):
    """购物车序列化器"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    product_image = serializers.SerializerMethodField()
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    subtotal = serializers.ReadOnlyField()
    address_info = serializers.SerializerMethodField()
    product_id = serializers.SerializerMethodField()  # 添加product_id字段

    class Meta:
        model = Cart
        fields = [
            'id', 'product', 'product_id', 'product_name', 'product_sku', 'product_image', 'product_price',
            'quantity', 'subtotal', 'address', 'address_info', 'notes', 'created_at'
        ]
    
    def get_product_id(self, obj):
        """获取商品ID，如果商品被删除则返回None"""
        return obj.product_id if obj.product else None
    
    def get_product_image(self, obj):
        """获取商品图片"""
        # 使用正确的关联名称获取图片
        images = obj.product.product_images.all()
        if images.exists():
            primary_image = images.filter(is_primary=True).first()
            if primary_image:
                return primary_image.get_image_url()
            else:
                # 如果没有主图，使用第一张图片
                first_image = images.first()
                if first_image:
                    return first_image.get_image_url()
        return None
    
    def get_address_info(self, obj):
        """获取地址信息"""
        if obj.address:
            return {
                'id': obj.address.id,
                'name': obj.address.name,
                'phone': obj.address.phone,
                'province': obj.address.province,
                'city': obj.address.city,
                'district': obj.address.district,
                'street': obj.address.street,
                'detail_address': obj.address.detail_address,
                'full_address': f"{obj.address.province}{obj.address.city}{obj.address.district}{obj.address.street}{obj.address.detail_address}",
                'is_default': obj.address.is_default
            }
        return None
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CartCreateSerializer(serializers.ModelSerializer):
    """购物车创建序列化器"""
    
    class Meta:
        model = Cart
        fields = ['product', 'quantity', 'address', 'notes']
    
    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data['product']
        quantity = validated_data['quantity']
        address = validated_data.get('address')
        notes = validated_data.get('notes', '')
        
        # 检查商品库存
        if product.stock < quantity:
            raise serializers.ValidationError("商品库存不足")
        
        # 直接创建新的购物车项目，不合并相同商品
        # 这样每个购物车项目都是独立的，可以有不同的地址
        cart_item = Cart.objects.create(
            user=user,
            product=product,
            quantity=quantity,
            address=address,
            notes=notes
        )
        
        return cart_item
    
    def validate_quantity(self, value):
        """验证数量"""
        if value <= 0:
            raise serializers.ValidationError("数量必须大于0")
        return value


class CartUpdateSerializer(serializers.ModelSerializer):
    """购物车更新序列化器"""
    
    class Meta:
        model = Cart
        fields = ['quantity']
    
    def validate_quantity(self, value):
        """验证数量"""
        if value <= 0:
            raise serializers.ValidationError("数量必须大于0")
        
        # 检查商品库存
        if value > self.instance.product.stock:
            raise serializers.ValidationError("商品库存不足")
        
        return value
