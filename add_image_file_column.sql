-- 为 products_productimage 表添加 image_file 字段
ALTER TABLE products_productimage 
ADD COLUMN image_file VARCHAR(100) NULL COMMENT '图片文件路径';

-- 更新 django_migrations 表，标记迁移为已应用
INSERT INTO django_migrations (app, name, applied) 
VALUES ('products', '0003_productimage_image_file', NOW())
ON DUPLICATE KEY UPDATE applied = NOW();
