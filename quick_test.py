#!/usr/bin/env python
"""
快速API测试
"""
import requests
import json

def quick_test():
    """快速测试API"""
    print("🚀 快速API测试...")
    
    # 测试健康检查
    try:
        response = requests.get("http://127.0.0.1:8000/health/", timeout=5)
        print(f"✅ 健康检查: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return
    
    # 测试商品API
    try:
        response = requests.get("http://127.0.0.1:8000/api/v1/products/", timeout=5)
        print(f"✅ 商品API: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   商品数量: {data.get('count', 0)}")
            print(f"   成功状态: {data.get('success', False)}")
        else:
            print(f"   响应: {response.text}")
    except Exception as e:
        print(f"❌ 商品API失败: {e}")
    
    # 测试分类API
    try:
        response = requests.get("http://127.0.0.1:8000/api/v1/products/categories/", timeout=5)
        print(f"✅ 分类API: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   分类数量: {data.get('count', 0)}")
            print(f"   成功状态: {data.get('success', False)}")
        else:
            print(f"   响应: {response.text}")
    except Exception as e:
        print(f"❌ 分类API失败: {e}")

if __name__ == "__main__":
    quick_test()
