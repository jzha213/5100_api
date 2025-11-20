#!/usr/bin/env python
"""
测试运行脚本
"""
import os
import sys
import subprocess
import argparse


def run_django_tests():
    """运行Django单元测试"""
    print("运行Django单元测试...")
    try:
        result = subprocess.run([
            sys.executable, 'manage.py', 'test', '--verbosity=2'
        ], capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"运行Django测试失败: {e}")
        return False


def run_api_tests(base_url="http://localhost:8000"):
    """运行API接口测试"""
    print(f"运行API接口测试 (服务器: {base_url})...")
    try:
        result = subprocess.run([
            sys.executable, 'tests/test_api.py', '--url', base_url
        ], capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"运行API测试失败: {e}")
        return False


def run_specific_test(test_name, base_url="http://localhost:8000"):
    """运行指定测试"""
    print(f"运行指定测试: {test_name} (服务器: {base_url})...")
    try:
        result = subprocess.run([
            sys.executable, 'tests/test_api.py', '--url', base_url, '--test', test_name
        ], capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"运行测试失败: {e}")
        return False


def check_server_running(base_url="http://localhost:8000"):
    """检查服务器是否运行"""
    import requests
    try:
        response = requests.get(f"{base_url}/health/", timeout=5)
        return response.status_code == 200
    except:
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='5100订水小程序测试运行脚本')
    parser.add_argument('--type', choices=['django', 'api', 'all'], default='all',
                       help='测试类型 (django: Django单元测试, api: API接口测试, all: 全部)')
    parser.add_argument('--url', default='http://localhost:8000',
                       help='API服务器地址 (默认: http://localhost:8000)')
    parser.add_argument('--test', help='运行指定API测试')
    parser.add_argument('--check-server', action='store_true',
                       help='只检查服务器是否运行')
    
    args = parser.parse_args()
    
    # 检查服务器状态
    if args.check_server:
        if check_server_running(args.url):
            print(f"✓ 服务器运行正常: {args.url}")
        else:
            print(f"✗ 服务器未运行或无法访问: {args.url}")
        return
    
    # 运行指定测试
    if args.test:
        success = run_specific_test(args.test, args.url)
        if not success:
            print(f"\n测试失败: {args.test}")
            sys.exit(1)
        else:
            print(f"\n测试通过: {args.test}")
        return
    
    # 运行测试
    results = []
    
    if args.type in ['django', 'all']:
        results.append(('Django单元测试', run_django_tests()))
    
    if args.type in ['api', 'all']:
        if check_server_running(args.url):
            results.append(('API接口测试', run_api_tests(args.url)))
        else:
            print(f"✗ 服务器未运行，跳过API测试: {args.url}")
            results.append(('API接口测试', False))
    
    # 输出结果
    print("\n" + "="*60)
    print("测试结果汇总:")
    print("="*60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("="*60)
    print(f"总计: {len(results)} 个测试套件")
    print(f"通过: {passed} 个")
    print(f"失败: {failed} 个")
    print(f"成功率: {passed/len(results)*100:.1f}%" if results else "0%")
    print("="*60)
    
    # 退出码
    sys.exit(0 if passed == len(results) else 1)


if __name__ == '__main__':
    main()
