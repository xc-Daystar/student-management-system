#!/usr/bin/env python3
"""
学生信息管理系统启动脚本
"""

import os
import sys
from app import app, init_db

def main():
    """主函数"""
    print("=== 学生信息管理系统 ===")
    print("正在启动系统...")
    
    # 初始化数据库
    try:
        init_db()
        print("✓ 数据库初始化成功")
    except Exception as e:
        print(f"✗ 数据库初始化失败: {e}")
        sys.exit(1)
    
    # 启动服务器
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    
    print(f"服务器地址: http://{host}:{port}")
    print("按 Ctrl+C 停止服务器")
    
    try:
        app.run(host=host, port=port, debug=True)
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"服务器启动失败: {e}")

if __name__ == '__main__':
    main()