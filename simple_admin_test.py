#!/usr/bin/env python
"""
简单的管理后台测试
"""
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_admin_page():
    """测试管理后台页面"""
    print("🔍 测试管理后台页面...")
    try:
        response = requests.get(f"{BASE_URL}/admin/")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # 检查是否有我们的自定义模型
            our_models = [
                '用户', '用户资料', '用户登录日志',
                '商品分类', '商品', '商品图片', '商品规格', '商品评价',
                '订单', '订单商品', '购物车', '订单状态日志',
                '用户地址',
                '优惠券', '用户优惠券', '优惠券使用记录'
            ]
            
            found_models = []
            for model in our_models:
                if model in content:
                    found_models.append(model)
            
            print(f"找到的模型: {found_models}")
            print(f"找到的模型数量: {len(found_models)}")
            
            if found_models:
                print("✅ 管理后台中有我们的自定义模型")
                return True
            else:
                print("❌ 管理后台中没有找到我们的自定义模型")
                return False
        else:
            print(f"❌ 无法访问管理后台，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 简单管理后台测试...")
    print("=" * 40)
    
    success = test_admin_page()
    
    print("\n" + "=" * 40)
    if success:
        print("✅ 管理后台配置成功！")
        print("\n📋 访问信息:")
        print("   🌐 管理后台: http://127.0.0.1:8000/admin/")
        print("   👤 用户名: jzha213")
        print("   🔑 密码: zjzj828")
        print("\n✨ 您可以在浏览器中访问管理后台查看所有自定义模型")
    else:
        print("❌ 管理后台配置可能存在问题")
    
    return success

if __name__ == "__main__":
    main()
