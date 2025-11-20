#!/bin/bash

echo "========================================"
echo "5100天然冰川矿泉水订水小程序后端API"
echo "快速启动脚本 (Linux/Mac)"
echo "========================================"
echo

# 检查Python环境
echo "检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未安装"
    exit 1
fi

echo "✓ Python环境正常"
echo

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

# 启动服务器
echo "启动服务器..."
python start_server.py
