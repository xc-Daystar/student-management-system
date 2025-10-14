from flask import Flask, render_template, request, jsonify
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 确保JSON不转义中文字符

# 数据库初始化
def init_db():
    conn = sqlite3.connect('student_management.db', check_same_thread=False)
    conn.text_factory = lambda x: x.decode('utf-8', 'ignore')  # 正确处理UTF-8编码
    cursor = conn.cursor()
    
    # 创建学生表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            gender TEXT NOT NULL,
            age INTEGER NOT NULL,
            class_name TEXT NOT NULL,
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
            credit INTEGER NOT NULL
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
            FOREIGN KEY (student_id) REFERENCES students (student_id),
            FOREIGN KEY (course_code) REFERENCES courses (course_code)
        )
    ''')
    
    conn.commit()
    conn.close()

# 主页路由
@app.route('/')
def index():
    return render_template('index.html')

# 学生管理API
@app.route('/api/students', methods=['GET', 'POST'])
def students_api():
    conn = sqlite3.connect('student_management.db', check_same_thread=False)
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
                    'created_at': student[6]
                })
            return jsonify(result)
        
        elif request.method == 'POST':
            # 添加新学生
            data = request.json
            try:
                cursor.execute('''
                    INSERT INTO students (student_id, name, gender, age, class_name)
                    VALUES (?, ?, ?, ?, ?)
                ''', (data['student_id'], data['name'], data['gender'], data['age'], data['class_name']))
                conn.commit()
                return jsonify({'message': '学生添加成功'}), 201
            except sqlite3.IntegrityError:
                return jsonify({'error': '学号已存在'}), 400
    finally:
        conn.close()

@app.route('/api/students/<student_id>', methods=['GET', 'PUT', 'DELETE'])
def student_api(student_id):
    conn = sqlite3.connect('student_management.db')
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
                    'created_at': student[6]
                })
            else:
                return jsonify({'error': '学生不存在'}), 404
        
        elif request.method == 'PUT':
            # 更新学生信息
            data = request.json
            cursor.execute('''
                UPDATE students SET name=?, gender=?, age=?, class_name=?
                WHERE student_id=?
            ''', (data['name'], data['gender'], data['age'], data['class_name'], student_id))
            conn.commit()
            return jsonify({'message': '学生信息更新成功'})
        
        elif request.method == 'DELETE':
            # 删除学生
            cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
            conn.commit()
            return jsonify({'message': '学生删除成功'})
    finally:
        conn.close()

# 课程管理API
@app.route('/api/courses', methods=['GET', 'POST'])
def courses_api():
    conn = sqlite3.connect('student_management.db')
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
                    'credit': course[4]
                })
            return jsonify(result)
        
        elif request.method == 'POST':
            data = request.json
            try:
                cursor.execute('''
                    INSERT INTO courses (course_code, course_name, teacher, credit)
                    VALUES (?, ?, ?, ?)
                ''', (data['course_code'], data['course_name'], data['teacher'], data['credit']))
                conn.commit()
                return jsonify({'message': '课程添加成功'}), 201
            except sqlite3.IntegrityError:
                return jsonify({'error': '课程代码已存在'}), 400
    finally:
        conn.close()

# 成绩管理API
@app.route('/api/grades', methods=['GET', 'POST'])
def grades_api():
    conn = sqlite3.connect('student_management.db')
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
                    'student_name': grade[5],
                    'course_name': grade[6]
                })
            return jsonify(result)
        
        elif request.method == 'POST':
            data = request.json
            cursor.execute('''
                INSERT INTO grades (student_id, course_code, score, semester)
                VALUES (?, ?, ?, ?)
            ''', (data['student_id'], data['course_code'], data['score'], data['semester']))
            conn.commit()
            return jsonify({'message': '成绩录入成功'}), 201
    finally:
        conn.close()

# 统计API
@app.route('/api/statistics/class-average')
def class_average():
    conn = sqlite3.connect('student_management.db')
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

if __name__ == '__main__':
    init_db()
    app.run(debug=True)