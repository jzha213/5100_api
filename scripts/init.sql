-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS `5100water` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE `5100water`;

-- 设置时区
SET time_zone = '+08:00';

-- 创建用户（如果需要）
-- CREATE USER IF NOT EXISTS 'water_user'@'%' IDENTIFIED BY 'water_password';
-- GRANT ALL PRIVILEGES ON 5100water.* TO 'water_user'@'%';
-- FLUSH PRIVILEGES;
