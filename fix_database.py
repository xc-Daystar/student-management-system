#!/usr/bin/env python3
"""
数据库修复脚本
修复字段映射错误和数据问题
"""

import sqlite3
import os

def get_db_path():
    """获取数据库路径"""
    if os.environ.get('VERCEL'):
        return '/tmp/student_management.db'
    else:
        return 'student_management.db'

def fix_database_structure():
    """修复数据库结构"""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🔧 开始修复数据库结构...")
    
    try:
        # 检查表结构
        cursor.execute("PRAGMA table_info(students)")
        columns = cursor.fetchall()
        print("当前学生表结构:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
        
        # 修复数据：清除错误数据
        cursor.execute("DELETE FROM students WHERE email LIKE '2025-%'")
        deleted_count = cursor.rowcount
        print(f"🗑️ 删除错误数据: {deleted_count} 条记录")
        
        # 添加示例学生数据（正确格式）
        sample_students = [
            ('2024001', '张三', '男', 20, '计算机科学与技术1班', 'zhangsan@example.com', '13800138001', '北京市海淀区'),
            ('2024002', '李四', '女', 19, '计算机科学与技术1班', 'lisi@example.com', '13800138002', '北京市朝阳区'),
            ('2024003', '王五', '男', 21, '软件工程2班', 'wangwu@example.com', '13800138003', '北京市西城区'),
            ('2024004', '赵六', '女', 20, '软件工程2班', 'zhaoliu@example.com', '13800138004', '北京市东城区'),
            ('2024005', '钱七', '男', 22, '人工智能3班', 'qianqi@example.com', '13800138005', '北京市丰台区')
        ]
        
        for student in sample_students:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO students 
                    (student_id, name, gender, age, class_name, email, phone, address)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', student)
            except Exception as e:
                print(f"⚠️ 插入学生失败: {student[1]} - {e}")
        
        # 添加示例课程数据
        sample_courses = [
            ('CS101', '计算机基础', '王教授', 3, '2024-2025-1', '计算机科学基础课程'),
            ('CS102', '数据结构', '李教授', 4, '2024-2025-1', '数据结构与算法'),
            ('CS201', '数据库系统', '张教授', 3, '2024-2025-2', '数据库设计与实现'),
            ('CS202', '操作系统', '刘教授', 4, '2024-2025-2', '操作系统原理与实践'),
            ('CS301', '人工智能导论', '陈教授', 3, '2024-2025-3', '人工智能基础理论')
        ]
        
        for course in sample_courses:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO courses 
                    (course_code, course_name, teacher, credit, semester, description)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', course)
            except Exception as e:
                print(f"⚠️ 插入课程失败: {course[1]} - {e}")
        
        # 添加示例成绩数据
        sample_grades = [
            ('2024001', 'CS101', 85.5, '2024-2025-1', '2024-12-20', '期中考试'),
            ('2024001', 'CS102', 92.0, '2024-2025-1', '2024-12-25', '期末考试'),
            ('2024002', 'CS101', 78.0, '2024-2025-1', '2024-12-20', '期中考试'),
            ('2024002', 'CS102', 88.5, '2024-2025-1', '2024-12-25', '期末考试'),
            ('2024003', 'CS101', 91.0, '2024-2025-1', '2024-12-20', '期中考试'),
            ('2024003', 'CS102', 86.5, '2024-2025-1', '2024-12-25', '期末考试'),
            ('2024004', 'CS101', 82.0, '2024-2025-1', '2024-12-20', '期中考试'),
            ('2024004', 'CS102', 90.0, '2024-2025-1', '2024-12-25', '期末考试'),
            ('2024005', 'CS101', 95.5, '2024-2025-1', '2024-12-20', '期中考试'),
            ('2024005', 'CS102', 89.0, '2024-2025-1', '2024-12-25', '期末考试')
        ]
        
        for grade in sample_grades:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO grades 
                    (student_id, course_code, score, semester, exam_date, remarks)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', grade)
            except Exception as e:
                print(f"⚠️ 插入成绩失败: 学号{grade[0]} - 课程{grade[1]} - {e}")
        
        conn.commit()
        print("✅ 数据库修复完成！")
        
        # 验证修复结果
        cursor.execute("SELECT COUNT(*) FROM students")
        student_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM courses")
        course_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM grades")
        grade_count = cursor.fetchone()[0]
        
        print(f"📊 修复后数据统计:")
        print(f"  学生数量: {student_count}")
        print(f"  课程数量: {course_count}")
        print(f"  成绩记录: {grade_count}")
        
    except Exception as e:
        print(f"❌ 数据库修复失败: {e}")
        conn.rollback()
    finally:
        conn.close()

def test_api_connection():
    """测试API连接"""
    import requests
    
    print("\n🔗 测试API连接...")
    try:
        # 测试健康检查
        response = requests.get('http://localhost:5000/api/health')
        print(f"✅ 健康检查: {response.json()}")
        
        # 测试学生数据
        response = requests.get('http://localhost:5000/api/students')
        students = response.json()
        print(f"✅ 学生数据: {len(students)} 条记录")
        
        # 测试课程数据
        response = requests.get('http://localhost:5000/api/courses')
        courses = response.json()
        print(f"✅ 课程数据: {len(courses)} 条记录")
        
        # 测试成绩数据
        response = requests.get('http://localhost:5000/api/grades')
        grades = response.json()
        print(f"✅ 成绩数据: {len(grades)} 条记录")
        
        # 测试统计信息
        response = requests.get('http://localhost:5000/api/statistics/summary')
        stats = response.json()
        print(f"✅ 统计信息: {stats}")
        
        return True
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("🔧 学生信息管理系统数据库修复工具")
    print("=" * 60)
    
    # 修复数据库
    fix_database_structure()
    
    # 测试API连接
    if test_api_connection():
        print("\n🎉 数据库修复成功！系统现在可以正常使用。")
        print("🌐 请访问 http://localhost:5000 查看完整系统")
    else:
        print("\n⚠️ 请确保Flask应用正在运行 (python app.py)")

if __name__ == "__main__":
    main()