from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.conf import settings
import os
import uuid
from PIL import Image
import io

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_avatar(request):
    """上传用户头像API"""
    try:
        # 检查是否有文件上传
        if 'avatar' not in request.FILES:
            return Response({
                'success': False,
                'message': '没有上传文件'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        avatar_file = request.FILES['avatar']
        
        # 验证文件类型
        allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if avatar_file.content_type not in allowed_types:
            return Response({
                'success': False,
                'message': '只支持 JPEG、PNG、GIF、WebP 格式的图片'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证文件大小 (最大5MB)
        max_size = 5 * 1024 * 1024  # 5MB
        if avatar_file.size > max_size:
            return Response({
                'success': False,
                'message': '图片大小不能超过5MB'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 生成唯一文件名
        file_extension = os.path.splitext(avatar_file.name)[1]
        unique_filename = f"avatar_{request.user.id}_{uuid.uuid4().hex}{file_extension}"
        
        # 保存到用户头像目录
        avatar_path = f"avatars/{unique_filename}"
        
        # 处理图片（压缩和调整大小）
        try:
            # 打开图片
            image = Image.open(avatar_file)
            
            # 转换为RGB模式（处理PNG透明背景）
            if image.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            
            # 调整图片大小（最大300x300）
            max_size = (300, 300)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # 保存处理后的图片
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            
            # 保存到存储
            saved_path = default_storage.save(avatar_path, output)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'图片处理失败: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 生成访问URL - 返回完整URL
        from django.conf import settings
        base_url = 'http://127.0.0.1:8000'  # 开发环境固定域名
        avatar_url = f"{base_url}{settings.MEDIA_URL}{saved_path}"
        
        # 更新用户头像
        user = request.user
        user.avatar_url = avatar_url
        user.save()
        
        return Response({
            'success': True,
            'message': '头像上传成功',
            'data': {
                'url': avatar_url,
                'filename': unique_filename
            }
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'上传失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
