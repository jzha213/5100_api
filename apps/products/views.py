from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Category, Product, ProductReview
from .serializers import (
    CategorySerializer, ProductListSerializer, ProductDetailSerializer,
    ProductCreateSerializer, ProductUpdateSerializer, ProductReviewSerializer,
    ProductReviewCreateSerializer
)


class CategoryListView(generics.ListAPIView):
    """商品分类列表"""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductListView(generics.ListAPIView):
    """商品列表"""
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_featured']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'sales_count', 'created_at']
    ordering = ['-created_at']


class ProductDetailView(generics.RetrieveAPIView):
    """商品详情"""
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # 记录商品浏览行为
        if request.user.is_authenticated:
            from apps.analytics.models import UserBehavior
            UserBehavior.objects.create(
                user=request.user,
                behavior_type='product_view',
                product=instance,
                page_url=request.build_absolute_uri(),
                page_title=instance.name
            )
        
        serializer = self.get_serializer(instance)
        return Response({
            'code': 200,
            'message': 'success',
            'data': serializer.data
        })


class ProductCreateView(generics.CreateAPIView):
    """商品创建"""
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [permissions.IsAdminUser]


class ProductUpdateView(generics.UpdateAPIView):
    """商品更新"""
    queryset = Product.objects.all()
    serializer_class = ProductUpdateSerializer
    permission_classes = [permissions.IsAdminUser]


class ProductReviewListView(generics.ListAPIView):
    """商品评价列表"""
    serializer_class = ProductReviewSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return ProductReview.objects.filter(product_id=product_id).order_by('-created_at')


class ProductReviewCreateView(generics.CreateAPIView):
    """商品评价创建"""
    serializer_class = ProductReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def featured_products(request):
    """推荐商品"""
    products = Product.objects.filter(is_active=True, is_featured=True).order_by('-created_at')[:10]
    serializer = ProductListSerializer(products, many=True)
    
    return Response({
        'code': 200,
        'message': 'success',
        'data': serializer.data
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_products(request):
    """搜索商品"""
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort', '-created_at')
    
    queryset = Product.objects.filter(is_active=True)
    
    if query:
        queryset = queryset.filter(name__icontains=query)
    
    if category_id:
        queryset = queryset.filter(category_id=category_id)
    
    if min_price:
        queryset = queryset.filter(price__gte=min_price)
    
    if max_price:
        queryset = queryset.filter(price__lte=max_price)
    
    # 排序
    if sort_by in ['price', '-price', 'sales_count', '-sales_count', 'created_at', '-created_at']:
        queryset = queryset.order_by(sort_by)
    
    # 分页
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 20))
    
    start = (page - 1) * page_size
    end = start + page_size
    
    products = queryset[start:end]
    total = queryset.count()
    
    serializer = ProductListSerializer(products, many=True)
    
    return Response({
        'code': 200,
        'message': 'success',
        'data': {
            'results': serializer.data,
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size
        }
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def product_recommendations(request, product_id):
    """商品推荐"""
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({
            'code': 404,
            'message': '商品不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # 推荐同分类的其他商品
    recommendations = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product_id).order_by('-sales_count')[:6]
    
    serializer = ProductListSerializer(recommendations, many=True)
    
    return Response({
        'code': 200,
        'message': 'success',
        'data': serializer.data
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_to_cart(request):
    """添加到购物车"""
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)
    
    if not product_id:
        return Response({
            'code': 400,
            'message': '商品ID不能为空'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        product = Product.objects.get(id=product_id, is_active=True)
    except Product.DoesNotExist:
        return Response({
            'code': 404,
            'message': '商品不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if product.stock < quantity:
        return Response({
            'code': 400,
            'message': '商品库存不足'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 添加到购物车
    from apps.orders.models import Cart
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        if cart_item.quantity > product.stock:
            cart_item.quantity = product.stock
        cart_item.save()
    
    # 记录用户行为
    from apps.analytics.models import UserBehavior
    UserBehavior.objects.create(
        user=request.user,
        behavior_type='add_to_cart',
        product=product,
        extra_data={'quantity': quantity}
    )
    
    return Response({
        'code': 200,
        'message': '已添加到购物车'
    })
