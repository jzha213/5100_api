#!/usr/bin/env python
"""
检查MySQL端口连接
"""
import pymysql
import socket

def check_mysql_ports():
    """检查常见的MySQL端口"""
    ports = [3306, 3307, 3308, 3309]
    host = '127.0.0.1'
    password = 'zjzj828'
    
    print("正在检查MySQL端口连接...")
    
    for port in ports:
        print(f"\n检查端口 {port}...")
        
        # 1. 检查端口是否开放
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                print(f"✅ 端口 {port} 开放")
                
                # 2. 尝试MySQL连接
                try:
                    connection = pymysql.connect(
                        host=host,
                        port=port,
                        user='root',
                        password=password,
                        charset='utf8mb4'
                    )
                    
                    cursor = connection.cursor()
                    cursor.execute("SELECT VERSION()")
                    version = cursor.fetchone()
                    print(f"✅ MySQL连接成功！版本: {version[0]}")
                    
                    # 检查数据库
                    cursor.execute("SHOW DATABASES LIKE '5100water'")
                    db_exists = cursor.fetchone()
                    
                    if db_exists:
                        print(f"✅ 数据库 '5100water' 存在")
                        cursor.execute("USE 5100water")
                        cursor.execute("SHOW TABLES")
                        tables = cursor.fetchall()
                        print(f"✅ 数据库中有 {len(tables)} 个表")
                    else:
                        print("❌ 数据库 '5100water' 不存在")
                        print("正在创建数据库...")
                        cursor.execute("CREATE DATABASE 5100water CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                        print("✅ 数据库创建成功")
                    
                    connection.close()
                    print(f"\n🎉 找到正确的MySQL端口: {port}")
                    return port
                    
                except Exception as e:
                    print(f"❌ MySQL连接失败: {e}")
            else:
                print(f"❌ 端口 {port} 关闭")
                
        except Exception as e:
            print(f"❌ 检查端口 {port} 失败: {e}")
    
    print("\n❌ 没有找到可用的MySQL端口")
    return None

def update_settings(port):
    """更新settings.py中的端口配置"""
    if port:
        print(f"\n正在更新settings.py中的端口为 {port}...")
        try:
            # 读取settings文件
            with open('config/settings/base.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 替换端口
            import re
            pattern = r"'PORT': '\d+'"
            replacement = f"'PORT': '{port}'"
            new_content = re.sub(pattern, replacement, content)
            
            # 写回文件
            with open('config/settings/base.py', 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ 端口已更新为 {port}")
            return True
        except Exception as e:
            print(f"❌ 更新端口失败: {e}")
            return False
    return False

def main():
    print("=" * 60)
    print("MySQL端口检查脚本")
    print("=" * 60)
    
    # 检查端口
    correct_port = check_mysql_ports()
    
    if correct_port:
        # 更新配置
        update_settings(correct_port)
        
        print("\n" + "=" * 60)
        print("端口检查完成！")
        print(f"正确的MySQL端口是: {correct_port}")
        print("配置文件已更新")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("没有找到可用的MySQL端口")
        print("请检查MySQL服务是否启动")
        print("=" * 60)

if __name__ == '__main__':
    main()
