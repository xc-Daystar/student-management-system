from http.server import BaseHTTPRequestHandler
import json
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def app():
    # 延迟导入以避免循环依赖
    from app import app as flask_app
    return flask_app

def handler(request):
    """Vercel Serverless函数处理程序"""
    # 获取Flask应用实例
    flask_app = app()
    
    # 构建WSGI环境
    environ = {
        'REQUEST_METHOD': request.method,
        'PATH_INFO': request.path,
        'QUERY_STRING': request.query_string or '',
        'CONTENT_TYPE': request.headers.get('Content-Type', ''),
        'CONTENT_LENGTH': request.headers.get('Content-Length', '0'),
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': request.body,
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
        'SERVER_NAME': 'vercel',
        'SERVER_PORT': '443',
    }
    
    # 添加HTTP头
    for key, value in request.headers.items():
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