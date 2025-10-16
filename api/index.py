from http.server import BaseHTTPRequestHandler
import json
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入Flask应用
from app import app as flask_app

def handler(request, context):
    """Vercel Serverless函数处理程序 - 正确格式"""
    try:
        # 设置环境变量
        os.environ['VERCEL'] = 'true'
        
        # 构建WSGI环境
        environ = {
            'REQUEST_METHOD': request.get('httpMethod', 'GET'),
            'PATH_INFO': request.get('path', '/'),
            'QUERY_STRING': request.get('queryStringParameters', '') or '',
            'CONTENT_TYPE': request.get('headers', {}).get('content-type', ''),
            'CONTENT_LENGTH': str(len(request.get('body', '') or '')),
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https',
            'wsgi.input': request.get('body', ''),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': True,
            'wsgi.run_once': False,
            'SERVER_NAME': 'vercel',
            'SERVER_PORT': '443',
        }
        
        # 添加HTTP头
        headers = request.get('headers', {})
        for key, value in headers.items():
            environ[f'HTTP_{key.upper().replace("-", "_")}'] = value
        
        # 处理请求
        with flask_app.request_context(environ):
            response = flask_app.full_dispatch_request()
            
            # 返回Vercel期望的格式
            return {
                'statusCode': response.status_code,
                'headers': dict(response.headers),
                'body': response.get_data(as_text=True)
            }
            
    except Exception as e:
        # 返回错误响应
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'Server error: {str(e)}'})
        }

# 兼容AWS Lambda格式
def lambda_handler(event, context):
    return handler(event, context)