from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Category, Product
from .serializers import CategorySerializer, ProductListSerializer, ProductDetailSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def product_list(request):
    """商品列表API"""
    products = Product.objects.filter(is_active=True)
    
    # 处理分类过滤
    category_id = request.GET.get('category')
    if category_id:
        try:
            category_id = int(category_id)
            products = products.filter(category_id=category_id)
        except (ValueError, TypeError):
            pass  # 如果category_id不是有效整数，忽略过滤
    
    # 处理推荐商品过滤
    is_featured = request.GET.get('is_featured')
    if is_featured is not None:
        if is_featured.lower() in ['true', '1', 'yes']:
            products = products.filter(is_featured=True)
        elif is_featured.lower() in ['false', '0', 'no']:
            products = products.filter(is_featured=False)
    
    # 处理搜索
    search = request.GET.get('search')
    if search:
        products = products.filter(name__icontains=search)
    
    # 处理排序
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by in ['price', '-price', 'sales_count', '-sales_count', 'created_at', '-created_at']:
        products = products.order_by(sort_by)
    else:
        products = products.order_by('-created_at')
    
    serializer = ProductListSerializer(products, many=True)
    return Response({
        'success': True,
        'data': serializer.data,
        'count': products.count()
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def category_list(request):
    """分类列表API"""
    categories = Category.objects.filter(is_active=True)
    serializer = CategorySerializer(categories, many=True)
    return Response({
        'success': True,
        'data': serializer.data,
        'count': categories.count()
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def product_detail(request, pk):
    """商品详情API"""
    try:
        product = Product.objects.get(pk=pk, is_active=True)
        serializer = ProductDetailSerializer(product)
        return Response({
            'success': True,
            'data': serializer.data
        })
    except Product.DoesNotExist:
        return Response({
            'success': False,
            'message': '商品不存在'
        }, status=404)
