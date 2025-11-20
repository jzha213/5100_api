#!/usr/bin/env python
"""
商品API测试脚本
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_product_list():
    """测试商品列表API"""
    print("🔍 测试商品列表API...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/products/", timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 商品列表API成功")
            print(f"   返回商品数量: {data.get('count', 0)}")
            print(f"   成功状态: {data.get('success', False)}")
            
            # 显示前3个商品信息
            products = data.get('data', [])
            if products:
                print("   商品信息:")
                for i, product in enumerate(products[:3]):
                    print(f"     {i+1}. {product.get('name', 'N/A')} - ¥{product.get('price', 'N/A')}")
            return True
        else:
            print(f"❌ 商品列表API失败: {response.status_code}")
            print(f"   响应内容: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 商品列表API异常: {e}")
        return False

def test_category_list():
    """测试分类列表API"""
    print("\n🔍 测试分类列表API...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/products/categories/", timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 分类列表API成功")
            print(f"   返回分类数量: {data.get('count', 0)}")
            print(f"   成功状态: {data.get('success', False)}")
            
            # 显示分类信息
            categories = data.get('data', [])
            if categories:
                print("   分类信息:")
                for i, category in enumerate(categories):
                    print(f"     {i+1}. {category.get('name', 'N/A')}")
            return True
        else:
            print(f"❌ 分类列表API失败: {response.status_code}")
            print(f"   响应内容: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 分类列表API异常: {e}")
        return False

def test_product_detail():
    """测试商品详情API"""
    print("\n🔍 测试商品详情API...")
    try:
        # 先获取商品列表，取第一个商品的ID
        list_response = requests.get(f"{BASE_URL}/api/v1/products/", timeout=10)
        if list_response.status_code == 200:
            products = list_response.json().get('data', [])
            if products:
                product_id = products[0].get('id')
                print(f"   测试商品ID: {product_id}")
                
                response = requests.get(f"{BASE_URL}/api/v1/products/{product_id}/", timeout=10)
                print(f"状态码: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ 商品详情API成功")
                    print(f"   商品名称: {data.get('data', {}).get('name', 'N/A')}")
                    print(f"   商品价格: ¥{data.get('data', {}).get('price', 'N/A')}")
                    print(f"   商品库存: {data.get('data', {}).get('stock', 'N/A')}")
                    return True
                else:
                    print(f"❌ 商品详情API失败: {response.status_code}")
                    print(f"   响应内容: {response.text}")
                    return False
            else:
                print("❌ 没有商品数据可供测试")
                return False
        else:
            print("❌ 无法获取商品列表")
            return False
    except Exception as e:
        print(f"❌ 商品详情API异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试5100订水商品API...")
    print("=" * 60)
    
    tests = [
        test_product_list,
        test_category_list,
        test_product_detail,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 商品API测试全部通过！")
    else:
        print("⚠️  部分测试失败，请检查API配置")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ 商品API运行正常！")
        print("📋 可用的API端点:")
        print("   - GET /api/v1/products/ (商品列表)")
        print("   - GET /api/v1/products/categories/ (分类列表)")
        print("   - GET /api/v1/products/{id}/ (商品详情)")
    else:
        print("\n❌ 商品API测试失败！")
