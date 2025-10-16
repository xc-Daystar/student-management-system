from http.server import BaseHTTPRequestHandler
import json
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def handler(event, context):
    """最简单的Vercel Serverless函数"""
    try:
        # 导入Flask应用（延迟导入避免循环依赖）
        from app import app as flask_app
        
        # 使用Flask测试客户端处理请求
        with flask_app.test_request_context(
            path=event.get('path', '/'),
            method=event.get('httpMethod', 'GET'),
            headers=event.get('headers', {}),
            data=event.get('body', '')
        ):
            response = flask_app.full_dispatch_request()
            
            return {
                'statusCode': response.status_code,
                'headers': dict(response.headers),
                'body': response.get_data(as_text=True)
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'Server error: {str(e)}'})
        }

# Vercel期望的函数
def lambda_handler(event, context):
    return handler(event, context)