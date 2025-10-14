from app import app
from flask import Response
import json

def handler(request, environ=None):
    # Vercel Serverless适配
    if request is None and environ is not None:
        # 本地测试模式
        with app.request_context(environ):
            response = app.full_dispatch_request()
            return {
                'statusCode': response.status_code,
                'headers': dict(response.headers),
                'body': response.get_data(as_text=True)
            }
    else:
        # Vercel环境
        path = request.path
        method = request.method
        
        # 构建WSGI环境
        environ = {
            'REQUEST_METHOD': method,
            'PATH_INFO': path,
            'QUERY_STRING': request.query_string.decode() if request.query_string else '',
            'CONTENT_TYPE': request.headers.get('Content-Type', ''),
            'CONTENT_LENGTH': request.headers.get('Content-Length', '0'),
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https',
            'wsgi.input': request.body,
            'wsgi.errors': None,
            'wsgi.multithread': False,
            'wsgi.multiprocess': True,
            'wsgi.run_once': False
        }
        
        # 添加HTTP头
        for key, value in request.headers.items():
            environ[f'HTTP_{key.upper().replace("-", "_")}'] = value
        
        with app.request_context(environ):
            response = app.full_dispatch_request()
            
            return Response(
                response.get_data(),
                status=response.status_code,
                headers=dict(response.headers)
            )