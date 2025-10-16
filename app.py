from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime
import os
import requests
from supabase import create_client
from typing import Union, Tuple

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 确保JSON不转义中文字符
CORS(app)  # 启用CORS支持

# Vercel环境适配
def get_db_path():
    if os.environ.get('VERCEL'):
        # Vercel环境使用临时文件
        return '/tmp/student_management.db'
    else:
        # 本地环境
        return 'student_management.db'

# Supabase配置 - 使用环境变量
SUPABASE_URL = os.environ.get('SUPABASE_URL', "https://uuhbirqghkmoqsugjcfh.supabase.co")
SUPABASE_KEY = os.environ.get('SUPABASE_ANON_KEY', "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV1aGJpcnFnaGttb3FzdWdqY2ZoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA1MDkxMzUsImV4cCI6MjA3NjA4NTEzNV0.vDvWe84JPFkN493mEBNv9B6wsda4bkmSGiODntmYRPk")

# 初始化Supabase客户端
supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Supabase客户端初始化失败: {e}")
        supabase = None

def get_supabase_client():
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Supabase连接失败: {e}")
        return None

# 数据库初始化
def init_db():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.text_factory = lambda x: x.decode('utf-8', 'ignore')  # 正确处理UTF-8编码
    cursor = conn.cursor()
    
    # 创建学生表（修复字段顺序）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            gender TEXT NOT NULL,
            age INTEGER NOT NULL,
            class_name TEXT NOT NULL,
            email TEXT DEFAULT '',
            phone TEXT DEFAULT '',
            address TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建课程表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_code TEXT UNIQUE NOT NULL,
            course_name TEXT NOT NULL,
            teacher TEXT NOT NULL,
            credit INTEGER NOT NULL,
            semester TEXT,
            description TEXT
        )
    ''')
    
    # 创建成绩表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            course_code TEXT NOT NULL,
            score REAL NOT NULL,
            semester TEXT NOT NULL,
            exam_date DATE,
            remarks TEXT,
            FOREIGN KEY (student_id) REFERENCES students (student_id),
            FOREIGN KEY (course_code) REFERENCES courses (course_code)
        )
    ''')
    
    # 创建用户表（用于系统管理）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'teacher',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 插入默认管理员用户
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password_hash, role) 
        VALUES (?, ?, ?)
    ''', ('admin', 'pbkdf2:sha256:260000$hash$default', 'admin'))
    
    conn.commit()
    conn.close()

# 主页路由
@app.route('/')
def index():
    return render_template('index.html')

# 学生管理API
@app.route('/api/students', methods=['GET', 'POST'])
def students_api() -> Union[Response, Tuple[Response, int]]:
    db_path = get_db_path()
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.text_factory = lambda x: x.decode('utf-8', 'ignore')  # 正确处理UTF-8编码
    cursor = conn.cursor()
    
    try:
        if request.method == 'GET':
            # 获取所有学生
            cursor.execute('SELECT * FROM students')
            students = cursor.fetchall()
            result = []
            for student in students:
                result.append({
                    'id': student[0],
                    'student_id': student[1],
                    'name': student[2],
                    'gender': student[3],
                    'age': student[4],
                    'class_name': student[5],
                    'email': student[6] if len(student) > 6 else '',
                    'phone': student[7] if len(student) > 7 else '',
                    'address': student[8] if len(student) > 8 else '',
                    'created_at': student[9] if len(student) > 9 else ''
                })
            return jsonify(result)
        
        elif request.method == 'POST':
            # 添加新学生
            data = request.json or {}
            try:
                cursor.execute('''
                    INSERT INTO students (student_id, name, gender, age, class_name, email, phone, address)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data.get('student_id', ''), data.get('name', ''), data.get('gender', ''), 
                    data.get('age', 0), data.get('class_name', ''), 
                    data.get('email', ''), data.get('phone', ''), data.get('address', '')
                ))
                conn.commit()
                return jsonify({'message': '学生添加成功'}), 201
            except sqlite3.IntegrityError:
                return jsonify({'error': '学号已存在'}), 400
    finally:
        conn.close()
    return jsonify({'error': '请求方法不支持'}), 405

@app.route('/api/students/<student_id>', methods=['GET', 'PUT', 'DELETE'])
def student_api(student_id) -> Union[Response, Tuple[Response, int]]:
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        if request.method == 'GET':
            # 获取特定学生信息
            cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
            student = cursor.fetchone()
            if student:
                return jsonify({
                    'id': student[0],
                    'student_id': student[1],
                    'name': student[2],
                    'gender': student[3],
                    'age': student[4],
                    'class_name': student[5],
                    'email': student[6] if len(student) > 6 else '',
                    'phone': student[7] if len(student) > 7 else '',
                    'address': student[8] if len(student) > 8 else '',
                    'created_at': student[9] if len(student) > 9 else ''
                })
            else:
                return jsonify({'error': '学生不存在'}), 404
        
        elif request.method == 'PUT':
            # 更新学生信息
            data = request.json or {}
            cursor.execute('''
                UPDATE students SET name=?, gender=?, age=?, class_name=?, email=?, phone=?, address=?
                WHERE student_id=?
            ''', (
                data.get('name', ''), data.get('gender', ''), data.get('age', 0), data.get('class_name', ''),
                data.get('email', ''), data.get('phone', ''), data.get('address', ''),
                student_id
            ))
            conn.commit()
            return jsonify({'message': '学生信息更新成功'})
        
        elif request.method == 'DELETE':
            # 删除学生
            cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
            conn.commit()
            return jsonify({'message': '学生删除成功'})
    finally:
        conn.close()
    return jsonify({'error': '请求方法不支持'}), 405

# 课程管理API
@app.route('/api/courses', methods=['GET', 'POST'])
def courses_api() -> Union[Response, Tuple[Response, int]]:
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        if request.method == 'GET':
            cursor.execute('SELECT * FROM courses')
            courses = cursor.fetchall()
            result = []
            for course in courses:
                result.append({
                    'id': course[0],
                    'course_code': course[1],
                    'course_name': course[2],
                    'teacher': course[3],
                    'credit': course[4],
                    'semester': course[5] if len(course) > 5 else '',
                    'description': course[6] if len(course) > 6 else ''
                })
            return jsonify(result)
        
        elif request.method == 'POST':
            data = request.json or {}
            try:
                cursor.execute('''
                    INSERT INTO courses (course_code, course_name, teacher, credit, semester, description)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    data.get('course_code', ''), data.get('course_name', ''), 
                    data.get('teacher', ''), data.get('credit', 0),
                    data.get('semester', ''), data.get('description', '')
                ))
                conn.commit()
                return jsonify({'message': '课程添加成功'}), 201
            except sqlite3.IntegrityError:
                return jsonify({'error': '课程代码已存在'}), 400
    finally:
        conn.close()
    return jsonify({'error': '请求方法不支持'}), 405

# 成绩管理API
@app.route('/api/grades', methods=['GET', 'POST'])
def grades_api() -> Union[Response, Tuple[Response, int]]:
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        if request.method == 'GET':
            cursor.execute('''
                SELECT g.*, s.name as student_name, c.course_name 
                FROM grades g 
                JOIN students s ON g.student_id = s.student_id 
                JOIN courses c ON g.course_code = c.course_code
            ''')
            grades = cursor.fetchall()
            result = []
            for grade in grades:
                result.append({
                    'id': grade[0],
                    'student_id': grade[1],
                    'course_code': grade[2],
                    'score': grade[3],
                    'semester': grade[4],
                    'exam_date': grade[5] if len(grade) > 5 else '',
                    'remarks': grade[6] if len(grade) > 6 else '',
                    'student_name': grade[7] if len(grade) > 7 else '',
                    'course_name': grade[8] if len(grade) > 8 else ''
                })
            return jsonify(result)
        
        elif request.method == 'POST':
            data = request.json or {}
            cursor.execute('''
                INSERT INTO grades (student_id, course_code, score, semester, exam_date, remarks)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                data.get('student_id', ''), data.get('course_code', ''), 
                data.get('score', 0), data.get('semester', ''),
                data.get('exam_date', ''), data.get('remarks', '')
            ))
            conn.commit()
            return jsonify({'message': '成绩录入成功'}), 201
    finally:
        conn.close()
    return jsonify({'error': '请求方法不支持'}), 405

# 统计API
@app.route('/api/statistics/class-average')
def class_average() -> Response:
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT s.class_name, AVG(g.score) as average_score
            FROM grades g
            JOIN students s ON g.student_id = s.student_id
            GROUP BY s.class_name
        ''')
        results = cursor.fetchall()
        
        statistics = []
        for result in results:
            statistics.append({
                'class_name': result[0],
                'average_score': round(result[1], 2)
            })
        
        return jsonify(statistics)
    finally:
        conn.close()

# 新增API：搜索学生
@app.route('/api/students/search/<keyword>')
def search_students(keyword) -> Response:
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT * FROM students 
            WHERE name LIKE ? OR student_id LIKE ? OR class_name LIKE ?
        ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
        students = cursor.fetchall()
        
        result = []
        for student in students:
            result.append({
                'id': student[0],
                'student_id': student[1],
                'name': student[2],
                'gender': student[3],
                'age': student[4],
                'class_name': student[5],
                'email': student[6] if len(student) > 6 else '',
                'phone': student[7] if len(student) > 7 else '',
                'address': student[8] if len(student) > 8 else '',
                'created_at': student[9] if len(student) > 9 else ''
            })
        return jsonify(result)
    finally:
        conn.close()

# 新增API：获取学生成绩详情
@app.route('/api/students/<student_id>/grades')
def student_grades(student_id) -> Union[Response, Tuple[Response, int]]:
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT g.*, c.course_name, c.teacher, c.credit
            FROM grades g
            JOIN courses c ON g.course_code = c.course_code
            WHERE g.student_id = ?
        ''', (student_id,))
        grades = cursor.fetchall()
        
        result = []
        for grade in grades:
            result.append({
                'id': grade[0],
                'course_code': grade[2],
                'course_name': grade[7],
                'teacher': grade[8],
                'credit': grade[9],
                'score': grade[3],
                'semester': grade[4],
                'exam_date': grade[5] if len(grade) > 5 else '',
                'remarks': grade[6] if len(grade) > 6 else ''
            })
        return jsonify(result)
    finally:
        conn.close()

# Supabase API接口
@app.route('/api/supabase/students', methods=['GET', 'POST'])
def supabase_students_api() -> Union[Response, Tuple[Response, int]]:
    try:
        if request.method == 'GET':
            # 从Supabase获取学生数据
            response = supabase.table('students').select('*').execute()
            return jsonify(response.data)
        
        elif request.method == 'POST':
            # 向Supabase添加学生
            data = request.json or {}
            response = supabase.table('students').insert(data).execute()
            return jsonify({'message': '学生添加成功', 'data': response.data}), 201
    except Exception as e:
        return jsonify({'error': f'Supabase操作失败: {str(e)}'}), 500
    return jsonify({'error': '请求方法不支持'}), 405

@app.route('/api/supabase/students/<student_id>', methods=['GET', 'PUT', 'DELETE'])
def supabase_student_api(student_id) -> Union[Response, Tuple[Response, int]]:
    try:
        if request.method == 'GET':
            # 获取特定学生信息
            response = supabase.table('students').select('*').eq('student_id', student_id).execute()
            if response.data:
                return jsonify(response.data[0])
            else:
                return jsonify({'error': '学生不存在'}), 404
        
        elif request.method == 'PUT':
            # 更新学生信息
            data = request.json or {}
            response = supabase.table('students').update(data).eq('student_id', student_id).execute()
            return jsonify({'message': '学生信息更新成功', 'data': response.data})
        
        elif request.method == 'DELETE':
            # 删除学生
            response = supabase.table('students').delete().eq('student_id', student_id).execute()
            return jsonify({'message': '学生删除成功'})
    except Exception as e:
        return jsonify({'error': f'Supabase操作失败: {str(e)}'}), 500
    return jsonify({'error': '请求方法不支持'}), 405

@app.route('/api/supabase/courses', methods=['GET', 'POST'])
def supabase_courses_api() -> Union[Response, Tuple[Response, int]]:
    try:
        if request.method == 'GET':
            response = supabase.table('courses').select('*').execute()
            return jsonify(response.data)
        
        elif request.method == 'POST':
            data = request.json or {}
            response = supabase.table('courses').insert(data).execute()
            return jsonify({'message': '课程添加成功', 'data': response.data}), 201
    except Exception as e:
        return jsonify({'error': f'Supabase操作失败: {str(e)}'}), 500
    return jsonify({'error': '请求方法不支持'}), 405

@app.route('/api/supabase/grades', methods=['GET', 'POST'])
def supabase_grades_api() -> Union[Response, Tuple[Response, int]]:
    try:
        if request.method == 'GET':
            response = supabase.table('grades').select('*').execute()
            return jsonify(response.data)
        
        elif request.method == 'POST':
            data = request.json or {}
            response = supabase.table('grades').insert(data).execute()
            return jsonify({'message': '成绩录入成功', 'data': response.data}), 201
    except Exception as e:
        return jsonify({'error': f'Supabase操作失败: {str(e)}'}), 500
    return jsonify({'error': '请求方法不支持'}), 405

# 新增API：系统健康检查
@app.route('/api/health')
def health_check() -> Response:
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'database': 'SQLite + Supabase'
    })

# Supabase状态检查API
@app.route('/api/supabase/status')
def supabase_status() -> Response:
    try:
        # 使用更简单的连接测试方法 - 直接检查Supabase客户端
        # 尝试获取Supabase的根端点来测试连接
        import requests as req
        test_url = f"{SUPABASE_URL}/rest/v1/"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }
        
        response = req.get(test_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return jsonify({
                'status': 'warning',
                'message': 'Supabase连接正常，但数据库表尚未创建。请运行supabase_setup.py初始化表结构。',
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'status': 'error',
                'message': f'Supabase连接失败，HTTP状态码: {response.status_code}',
                'timestamp': datetime.now().isoformat()
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Supabase连接失败: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

# 新增API：数据统计
@app.route('/api/statistics/summary')
def statistics_summary() -> Response:
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 学生总数
        cursor.execute('SELECT COUNT(*) FROM students')
        total_students = cursor.fetchone()[0]
        
        # 课程总数
        cursor.execute('SELECT COUNT(*) FROM courses')
        total_courses = cursor.fetchone()[0]
        
        # 成绩记录总数
        cursor.execute('SELECT COUNT(*) FROM grades')
        total_grades = cursor.fetchone()[0]
        
        # 班级数量
        cursor.execute('SELECT COUNT(DISTINCT class_name) FROM students')
        total_classes = cursor.fetchone()[0]
        
        return jsonify({
            'total_students': total_students,
            'total_courses': total_courses,
            'total_grades': total_grades,
            'total_classes': total_classes
        })
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)