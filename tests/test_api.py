#!/usr/bin/env python
"""
API接口测试脚本
"""
import requests
import json
import time
from typing import Dict, Any


class APITester:
    """API测试类"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None
        self.user_id = None
        
    def make_request(self, method: str, endpoint: str, data: Dict[Any, Any] = None, 
                    headers: Dict[str, str] = None) -> requests.Response:
        """发送HTTP请求"""
        url = f"{self.base_url}{endpoint}"
        
        default_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        if self.token:
            default_headers['Authorization'] = f'Bearer {self.token}'
        
        if headers:
            default_headers.update(headers)
        
        if method.upper() == 'GET':
            response = self.session.get(url, headers=default_headers, params=data)
        elif method.upper() == 'POST':
            response = self.session.post(url, headers=default_headers, json=data)
        elif method.upper() == 'PUT':
            response = self.session.put(url, headers=default_headers, json=data)
        elif method.upper() == 'DELETE':
            response = self.session.delete(url, headers=default_headers, json=data)
        else:
            raise ValueError(f"不支持的HTTP方法: {method}")
        
        return response
    
    def print_response(self, response: requests.Response, title: str = ""):
        """打印响应结果"""
        print(f"\n{'='*50}")
        if title:
            print(f"测试: {title}")
        print(f"URL: {response.url}")
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            print(f"响应内容: {json.dumps(response_json, indent=2, ensure_ascii=False)}")
        except:
            print(f"响应内容: {response.text}")
        
        print('='*50)
    
    def test_health_check(self):
        """健康检查测试"""
        print("开始健康检查测试...")
        response = self.make_request('GET', '/health/')
        self.print_response(response, "健康检查")
        return response.status_code == 200
    
    def test_user_register(self):
        """用户注册测试"""
        print("开始用户注册测试...")
        data = {
            "username": "testuser001",
            "nickname": "测试用户",
            "phone": "13800138001",
            "password": "test123456",
            "password_confirm": "test123456"
        }
        response = self.make_request('POST', '/api/v1/auth/register/', data)
        self.print_response(response, "用户注册")
        
        if response.status_code == 201:
            result = response.json()
            if result.get('data', {}).get('tokens'):
                self.token = result['data']['tokens']['access']
                self.user_id = result['data']['user']['id']
                return True
        return False
    
    def test_wechat_login(self):
        """微信登录测试"""
        print("开始微信登录测试...")
        data = {
            "code": "mock_wechat_code_001"
        }
        response = self.make_request('POST', '/api/v1/auth/wechat/login/', data)
        self.print_response(response, "微信登录")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('data', {}).get('tokens'):
                self.token = result['data']['tokens']['access']
                self.user_id = result['data']['user']['id']
                return True
        return False
    
    def test_user_profile(self):
        """用户资料测试"""
        if not self.token:
            print("跳过用户资料测试，未登录")
            return False
        
        print("开始用户资料测试...")
        
        # 获取用户资料
        response = self.make_request('GET', '/api/v1/users/profile/')
        self.print_response(response, "获取用户资料")
        
        # 更新用户资料
        update_data = {
            "nickname": "更新的昵称",
            "gender": 1,
            "profile": {
                "real_name": "真实姓名",
                "address": "测试地址"
            }
        }
        response = self.make_request('PUT', '/api/v1/users/update/', update_data)
        self.print_response(response, "更新用户资料")
        
        return response.status_code == 200
    
    def test_product_categories(self):
        """商品分类测试"""
        print("开始商品分类测试...")
        response = self.make_request('GET', '/api/v1/products/categories/')
        self.print_response(response, "获取商品分类")
        return response.status_code == 200
    
    def test_products_list(self):
        """商品列表测试"""
        print("开始商品列表测试...")
        
        # 获取商品列表
        params = {
            'page': 1,
            'page_size': 10
        }
        response = self.make_request('GET', '/api/v1/products/', params)
        self.print_response(response, "获取商品列表")
        
        if response.status_code == 200:
            result = response.json()
            products = result.get('data', {}).get('results', [])
            if products:
                # 测试商品详情
                product_id = products[0]['id']
                response = self.make_request('GET', f'/api/v1/products/{product_id}/')
                self.print_response(response, "获取商品详情")
                return response.status_code == 200
        
        return response.status_code == 200
    
    def test_address_management(self):
        """地址管理测试"""
        if not self.token:
            print("跳过地址管理测试，未登录")
            return False
        
        print("开始地址管理测试...")
        
        # 创建地址
        address_data = {
            "name": "张三",
            "phone": "13800138001",
            "province": "北京市",
            "city": "北京市",
            "district": "朝阳区",
            "street": "三里屯街道",
            "detail_address": "三里屯SOHO A座1001",
            "longitude": 116.407526,
            "latitude": 39.904030,
            "is_default": True
        }
        response = self.make_request('POST', '/api/v1/addresses/', address_data)
        self.print_response(response, "创建地址")
        
        if response.status_code == 201:
            address_id = response.json()['data']['id']
            
            # 获取地址列表
            response = self.make_request('GET', '/api/v1/addresses/')
            self.print_response(response, "获取地址列表")
            
            # 更新地址
            update_data = {
                "name": "李四",
                "phone": "13800138002",
                "detail_address": "三里屯SOHO A座1002"
            }
            response = self.make_request('PUT', f'/api/v1/addresses/{address_id}/', update_data)
            self.print_response(response, "更新地址")
            
            return True
        
        return False
    
    def test_cart_management(self):
        """购物车管理测试"""
        if not self.token:
            print("跳过购物车管理测试，未登录")
            return False
        
        print("开始购物车管理测试...")
        
        # 先获取商品列表，选择第一个商品
        response = self.make_request('GET', '/api/v1/products/')
        if response.status_code != 200:
            return False
        
        products = response.json().get('data', {}).get('results', [])
        if not products:
            print("没有可用商品")
            return False
        
        product_id = products[0]['id']
        
        # 添加到购物车
        cart_data = {
            "product": product_id,
            "quantity": 2
        }
        response = self.make_request('POST', '/api/v1/orders/cart/create/', cart_data)
        self.print_response(response, "添加到购物车")
        
        if response.status_code == 201:
            # 获取购物车列表
            response = self.make_request('GET', '/api/v1/orders/cart/')
            self.print_response(response, "获取购物车列表")
            
            # 获取购物车汇总
            response = self.make_request('GET', '/api/v1/orders/cart/summary/')
            self.print_response(response, "获取购物车汇总")
            
            return True
        
        return False
    
    def test_order_creation(self):
        """订单创建测试"""
        if not self.token:
            print("跳过订单创建测试，未登录")
            return False
        
        print("开始订单创建测试...")
        
        # 先确保有地址和购物车商品
        # 这里简化处理，直接创建订单
        order_data = {
            "address_id": 1,  # 假设地址ID为1
            "items": [
                {
                    "product_id": 1,  # 假设商品ID为1
                    "quantity": 1
                }
            ],
            "remark": "测试订单"
        }
        response = self.make_request('POST', '/api/v1/orders/create/', order_data)
        self.print_response(response, "创建订单")
        
        if response.status_code == 201:
            order_id = response.json()['data']['id']
            
            # 获取订单列表
            response = self.make_request('GET', '/api/v1/orders/')
            self.print_response(response, "获取订单列表")
            
            # 获取订单详情
            response = self.make_request('GET', f'/api/v1/orders/{order_id}/')
            self.print_response(response, "获取订单详情")
            
            return True
        
        return False
    
    def test_payment_creation(self):
        """支付创建测试"""
        if not self.token:
            print("跳过支付创建测试，未登录")
            return False
        
        print("开始支付创建测试...")
        
        payment_data = {
            "order_id": 1,  # 假设订单ID为1
            "payment_type": "wechat"
        }
        response = self.make_request('POST', '/api/v1/payments/create/', payment_data)
        self.print_response(response, "创建支付")
        
        return response.status_code == 201
    
    def test_coupon_management(self):
        """优惠券管理测试"""
        print("开始优惠券管理测试...")
        
        # 获取优惠券列表
        response = self.make_request('GET', '/api/v1/coupons/')
        self.print_response(response, "获取优惠券列表")
        
        if self.token and response.status_code == 200:
            coupons = response.json().get('data', [])
            if coupons:
                coupon_id = coupons[0]['id']
                
                # 领取优惠券
                coupon_data = {
                    "coupon_id": coupon_id
                }
                response = self.make_request('POST', '/api/v1/coupons/user/create/', coupon_data)
                self.print_response(response, "领取优惠券")
                
                # 获取用户优惠券列表
                response = self.make_request('GET', '/api/v1/coupons/user/')
                self.print_response(response, "获取用户优惠券列表")
                
                return True
        
        return response.status_code == 200
    
    def test_notifications(self):
        """通知测试"""
        if not self.token:
            print("跳过通知测试，未登录")
            return False
        
        print("开始通知测试...")
        
        # 获取消息列表
        response = self.make_request('GET', '/api/v1/notifications/messages/')
        self.print_response(response, "获取消息列表")
        
        # 获取消息统计
        response = self.make_request('GET', '/api/v1/notifications/messages/stats/')
        self.print_response(response, "获取消息统计")
        
        return response.status_code == 200
    
    def test_analytics(self):
        """数据分析测试"""
        if not self.token:
            print("跳过数据分析测试，未登录")
            return False
        
        print("开始数据分析测试...")
        
        # 记录用户行为
        behavior_data = {
            "behavior_type": "page_view",
            "page_url": "https://example.com/test",
            "page_title": "测试页面"
        }
        response = self.make_request('POST', '/api/v1/analytics/behaviors/record/', behavior_data)
        self.print_response(response, "记录用户行为")
        
        return response.status_code == 200
    
    def run_all_tests(self):
        """运行所有测试"""
        print("开始运行API接口测试...")
        print(f"测试服务器: {self.base_url}")
        
        test_results = []
        
        # 基础功能测试
        test_results.append(("健康检查", self.test_health_check()))
        test_results.append(("商品分类", self.test_product_categories()))
        test_results.append(("商品列表", self.test_products_list()))
        test_results.append(("优惠券管理", self.test_coupon_management()))
        
        # 用户功能测试
        test_results.append(("用户注册", self.test_user_register()))
        test_results.append(("微信登录", self.test_wechat_login()))
        test_results.append(("用户资料", self.test_user_profile()))
        test_results.append(("地址管理", self.test_address_management()))
        test_results.append(("购物车管理", self.test_cart_management()))
        test_results.append(("订单创建", self.test_order_creation()))
        test_results.append(("支付创建", self.test_payment_creation()))
        test_results.append(("通知功能", self.test_notifications()))
        test_results.append(("数据分析", self.test_analytics()))
        
        # 输出测试结果
        print("\n" + "="*60)
        print("测试结果汇总:")
        print("="*60)
        
        passed = 0
        failed = 0
        
        for test_name, result in test_results:
            status = "✓ 通过" if result else "✗ 失败"
            print(f"{test_name:20} {status}")
            if result:
                passed += 1
            else:
                failed += 1
        
        print("="*60)
        print(f"总计: {len(test_results)} 个测试")
        print(f"通过: {passed} 个")
        print(f"失败: {failed} 个")
        print(f"成功率: {passed/len(test_results)*100:.1f}%")
        print("="*60)
        
        return passed == len(test_results)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='5100订水小程序API测试脚本')
    parser.add_argument('--url', default='http://localhost:8000', 
                       help='API服务器地址 (默认: http://localhost:8000)')
    parser.add_argument('--test', help='运行指定测试 (例如: user_register)')
    
    args = parser.parse_args()
    
    tester = APITester(args.url)
    
    if args.test:
        # 运行指定测试
        test_method = getattr(tester, f'test_{args.test}', None)
        if test_method:
            result = test_method()
            print(f"\n测试结果: {'通过' if result else '失败'}")
        else:
            print(f"未找到测试方法: test_{args.test}")
    else:
        # 运行所有测试
        success = tester.run_all_tests()
        exit(0 if success else 1)


if __name__ == '__main__':
    main()
