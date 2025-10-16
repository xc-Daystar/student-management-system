from flask import Flask
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 创建Flask应用实例
app = Flask(__name__)

# 导入主应用
from app import app as main_app

# Vercel Serverless函数入口
def handler(request, context):
    """Vercel Serverless函数处理程序"""
    try:
        # 设置环境变量
        os.environ['VERCEL'] = 'true'
        
        # 构建WSGI环境
        environ = {
            'REQUEST_METHOD': request['httpMethod'],
            'PATH_INFO': request['path'],
            'QUERY_STRING': request.get('rawQuery', ''),
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
        with main_app.request_context(environ):
            response = main_app.full_dispatch_request()
            
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
            'body': f'{{"error": "Server error: {str(e)}"}}'
        }

# 兼容旧版Vercel函数格式
def lambda_handler(event, context):
    return handler(event, context)