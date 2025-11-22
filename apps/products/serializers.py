from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductSpecification, ProductReview


class CategorySerializer(serializers.ModelSerializer):
    """商品分类序列化器"""
    children = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()  # 改为 SerializerMethodField 以使用 get_icon_url
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'icon', 'description', 'sort_order', 'is_active', 'children']
    
    def get_icon(self, obj):
        """获取分类图标URL，优先使用本地文件"""
        return obj.get_icon_url()
    
    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializer(obj.children.all(), many=True).data
        return []


class ProductImageSerializer(serializers.ModelSerializer):
    """商品图片序列化器"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image_url', 'alt_text', 'sort_order', 'is_primary']
    
    def get_image_url(self, obj):
        """获取图片URL，优先使用本地文件"""
        return obj.get_image_url()


class ProductSpecificationSerializer(serializers.ModelSerializer):
    """商品规格序列化器"""
    
    class Meta:
        model = ProductSpecification
        fields = ['id', 'name', 'value', 'sort_order']


class ProductReviewSerializer(serializers.ModelSerializer):
    """商品评价序列化器"""
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    user_avatar = serializers.URLField(source='user.avatar_url', read_only=True)
    
    class Meta:
        model = ProductReview
        fields = [
            'id', 'user_nickname', 'user_avatar', 'rating', 'content', 
            'images', 'is_anonymous', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ProductListSerializer(serializers.ModelSerializer):
    """商品列表序列化器"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    discount_rate = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'price', 'original_price', 'discount_rate',
            'stock', 'sales_count', 'category_name', 'primary_image', 
            'is_featured', 'sort_order', 'created_at'
        ]
    
    def get_primary_image(self, obj):
        primary_image = obj.product_images.filter(is_primary=True).first()
        if primary_image:
            return primary_image.get_image_url()
        # 如果没有主图，返回第一张图片
        first_image = obj.product_images.first()
        if first_image:
            return first_image.get_image_url()
        # 如果没有图片，返回默认图片
        return '/assets/images/default-product.svg'


class ProductDetailSerializer(serializers.ModelSerializer):
    """商品详情序列化器"""
    category = CategorySerializer(read_only=True)
    images = serializers.SerializerMethodField()
    specifications = serializers.SerializerMethodField()  # 改为 SerializerMethodField
    reviews = ProductReviewSerializer(many=True, read_only=True)
    discount_rate = serializers.ReadOnlyField()
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'sku', 'price', 'original_price', 
            'discount_rate', 'stock', 'sales_count', 'weight', 'volume',
            'category', 'images', 'specifications', 'reviews',
            'average_rating', 'review_count', 'is_active', 'is_featured',
            'created_at', 'updated_at'
        ]
    
    def get_specifications(self, obj):
        """处理规格数据，支持JSONField和关联对象两种格式"""
        if hasattr(obj, 'product_specifications') and obj.product_specifications.exists():
            # 如果有关联的ProductSpecification对象，使用序列化器
            return ProductSpecificationSerializer(obj.product_specifications.all(), many=True).data
        elif obj.specifications:
            # 如果是JSONField存储的字典数据，直接返回
            if isinstance(obj.specifications, dict):
                return [{'name': k, 'value': v} for k, v in obj.specifications.items()]
        return []
    
    def get_images(self, obj):
        """获取商品图片，如果没有图片则返回默认图片"""
        images = obj.product_images.all()
        if images.exists():
            return ProductImageSerializer(images, many=True).data
        else:
            # 如果没有图片，返回默认图片
            return [{
                'id': 0,
                'image_url': '/assets/images/default-product.svg',
                'alt_text': '默认商品图片',
                'sort_order': 0,
                'is_primary': True
            }]
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            total_rating = sum(review.rating for review in reviews)
            return round(total_rating / len(reviews), 1)
        return 0
    
    def get_review_count(self, obj):
        return obj.reviews.count()


class ProductCreateSerializer(serializers.ModelSerializer):
    """商品创建序列化器"""
    images = ProductImageSerializer(many=True, required=False)
    specifications = ProductSpecificationSerializer(many=True, required=False)
    
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'category', 'sku', 'price', 'original_price',
            'stock', 'weight', 'volume', 'images', 'specifications',
            'is_active', 'is_featured', 'sort_order'
        ]
    
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        specifications_data = validated_data.pop('specifications', [])
        
        product = Product.objects.create(**validated_data)
        
        # 创建商品图片
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)
        
        # 创建商品规格
        for spec_data in specifications_data:
            ProductSpecification.objects.create(product=product, **spec_data)
        
        return product


class ProductUpdateSerializer(serializers.ModelSerializer):
    """商品更新序列化器"""
    images = ProductImageSerializer(many=True, required=False)
    specifications = ProductSpecificationSerializer(many=True, required=False)
    
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'category', 'sku', 'price', 'original_price',
            'stock', 'weight', 'volume', 'images', 'specifications',
            'is_active', 'is_featured', 'sort_order'
        ]
    
    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        specifications_data = validated_data.pop('specifications', [])
        
        # 更新商品基本信息
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # 更新商品图片
        if images_data:
            # 删除原有图片
            instance.product_images.all().delete()
            # 创建新图片
            for image_data in images_data:
                ProductImage.objects.create(product=instance, **image_data)
        
        # 更新商品规格
        if specifications_data:
            # 删除原有规格
            instance.specifications.all().delete()
            # 创建新规格
            for spec_data in specifications_data:
                ProductSpecification.objects.create(product=instance, **spec_data)
        
        return instance


class ProductReviewCreateSerializer(serializers.ModelSerializer):
    """商品评价创建序列化器"""
    
    class Meta:
        model = ProductReview
        fields = ['product', 'rating', 'content', 'images', 'is_anonymous']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
