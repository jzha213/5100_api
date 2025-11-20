-- 修改 image_url 字段允许为空
ALTER TABLE products_productimage 
MODIFY COLUMN image_url VARCHAR(200) NULL;
