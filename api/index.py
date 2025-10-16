from flask import Flask, request, jsonify
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入Flask应用
from app import app as flask_app

def lambda_handler(event, context):
    """简化的Vercel Serverless函数适配器"""
    try:
        # 创建Flask测试客户端
        with flask_app.test_client() as client:
            # 构建请求
            method = event.get('httpMethod', 'GET')
            path = event.get('path', '/')
            headers = event.get('headers', {})
            body = event.get('body', '')
            
            # 发送请求
            response = client.open(
                path=path,
                method=method,
                headers=headers,
                data=body,
                content_type=headers.get('content-type', 'application/json')
            )
            
            # 返回响应
            return {
                'statusCode': response.status_code,
                'headers': dict(response.headers),
                'body': response.get_data(as_text=True)
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': f'{{"error": "Server error: {str(e)}"}}'
        }