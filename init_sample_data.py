#!/usr/bin/env python3
"""
学生信息管理系统示例数据初始化脚本
"""

import sqlite3
import requests
import json

# Flask应用URL
BASE_URL = "http://localhost:5000"

# 示例数据
SAMPLE_STUDENTS = [
    {
        "student_id": "2024001",
        "name": "张三",
        "gender": "男",
        "age": 20,
        "class_name": "计算机科学与技术1班",
        "email": "zhangsan@example.com",
        "phone": "13800138001",
        "address": "北京市海淀区"
    },
    {
        "student_id": "2024002",
        "name": "李四",
        "gender": "女",
        "age": 19,
        "class_name": "计算机科学与技术1班",
        "email": "lisi@example.com",
        "phone": "13800138002",
        "address": "北京市朝阳区"
    },
    {
        "student_id": "2024003",
        "name": "王五",
        "gender": "男",
        "age": 21,
        "class_name": "软件工程2班",
        "email": "wangwu@example.com",
        "phone": "13800138003",
        "address": "北京市西城区"
    },
    {
        "student_id": "2024004",
        "name": "赵六",
        "gender": "女",
        "age": 20,
        "class_name": "软件工程2班",
        "email": "zhaoliu@example.com",
        "phone": "13800138004",
        "address": "北京市东城区"
    },
    {
        "student_id": "2024005",
        "name": "钱七",
        "gender": "男",
        "age": 22,
        "class_name": "人工智能3班",
        "email": "qianqi@example.com",
        "phone": "13800138005",
        "address": "北京市丰台区"
    }
]

SAMPLE_COURSES = [
    {
        "course_code": "CS101",
        "course_name": "计算机基础",
        "teacher": "王教授",
        "credit": 3,
        "semester": "2024-2025-1",
        "description": "计算机科学基础课程"
    },
    {
        "course_code": "CS102",
        "course_name": "数据结构",
        "teacher": "李教授",
        "credit": 4,
        "semester": "2024-2025-1",
        "description": "数据结构与算法"
    },
    {
        "course_code": "CS201",
        "course_name": "数据库系统",
        "teacher": "张教授",
        "credit": 3,
        "semester": "2024-2025-2",
        "description": "数据库设计与实现"
    },
    {
        "course_code": "CS202",
        "course_name": "操作系统",
        "teacher": "刘教授",
        "credit": 4,
        "semester": "2024-2025-2",
        "description": "操作系统原理与实践"
    },
    {
        "course_code": "CS301",
        "course_name": "人工智能导论",
        "teacher": "陈教授",
        "credit": 3,
        "semester": "2024-2025-3",
        "description": "人工智能基础理论"
    }
]

SAMPLE_GRADES = [
    {"student_id": "2024001", "course_code": "CS101", "score": 85.5, "semester": "2024-2025-1"},
    {"student_id": "2024001", "course_code": "CS102", "score": 92.0, "semester": "2024-2025-1"},
    {"student_id": "2024002", "course_code": "CS101", "score": 78.0, "semester": "2024-2025-1"},
    {"student_id": "2024002", "course_code": "CS102", "score": 88.5, "semester": "2024-2025-1"},
    {"student_id": "2024003", "course_code": "CS101", "score": 91.0, "semester": "2024-2025-1"},
    {"student_id": "2024003", "course_code": "CS102", "score": 86.5, "semester": "2024-2025-1"},
    {"student_id": "2024004", "course_code": "CS101", "score": 82.0, "semester": "2024-2025-1"},
    {"student_id": "2024004", "course_code": "CS102", "score": 90.0, "semester": "2024-2025-1"},
    {"student_id": "2024005", "course_code": "CS101", "score": 95.5, "semester": "2024-2025-1"},
    {"student_id": "2024005", "course_code": "CS102", "score": 89.0, "semester": "2024-2025-1"}
]

def test_connection():
    """测试Flask应用连接"""
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print("✅ Flask应用连接正常")
            return True
        else:
            print("❌ Flask应用连接失败")
            return False
    except Exception as e:
        print(f"❌ 无法连接到Flask应用: {e}")
        return False

def add_students():
    """添加示例学生数据"""
    print("\n👨‍🎓 添加示例学生数据...")
    success_count = 0
    
    for student in SAMPLE_STUDENTS:
        try:
            response = requests.post(f"{BASE_URL}/api/students", json=student)
            if response.status_code == 201:
                print(f"✅ 添加学生: {student['name']} ({student['student_id']})")
                success_count += 1
            else:
                print(f"⚠️ 学生已存在或添加失败: {student['name']}")
        except Exception as e:
            print(f"❌ 添加学生失败: {student['name']} - {e}")
    
    print(f"📊 学生数据添加完成: {success_count}/{len(SAMPLE_STUDENTS)}")
    return success_count

def add_courses():
    """添加示例课程数据"""
    print("\n📚 添加示例课程数据...")
    success_count = 0
    
    for course in SAMPLE_COURSES:
        try:
            response = requests.post(f"{BASE_URL}/api/courses", json=course)
            if response.status_code == 201:
                print(f"✅ 添加课程: {course['course_name']} ({course['course_code']})")
                success_count += 1
            else:
                print(f"⚠️ 课程已存在或添加失败: {course['course_name']}")
        except Exception as e:
            print(f"❌ 添加课程失败: {course['course_name']} - {e}")
    
    print(f"📊 课程数据添加完成: {success_count}/{len(SAMPLE_COURSES)}")
    return success_count

def add_grades():
    """添加示例成绩数据"""
    print("\n📊 添加示例成绩数据...")
    success_count = 0
    
    for grade in SAMPLE_GRADES:
        try:
            response = requests.post(f"{BASE_URL}/api/grades", json=grade)
            if response.status_code == 201:
                print(f"✅ 添加成绩: 学号{grade['student_id']} - 课程{grade['course_code']} - {grade['score']}分")
                success_count += 1
            else:
                print(f"⚠️ 成绩添加失败: 学号{grade['student_id']} - 课程{grade['course_code']}")
        except Exception as e:
            print(f"❌ 添加成绩失败: 学号{grade['student_id']} - {e}")
    
    print(f"📊 成绩数据添加完成: {success_count}/{len(SAMPLE_GRADES)}")
    return success_count

def check_data():
    """检查数据添加结果"""
    print("\n🔍 检查数据添加结果...")
    
    try:
        # 检查学生数据
        response = requests.get(f"{BASE_URL}/api/students")
        students = response.json()
        print(f"📊 当前学生数量: {len(students)}")
        
        # 检查课程数据
        response = requests.get(f"{BASE_URL}/api/courses")
        courses = response.json()
        print(f"📊 当前课程数量: {len(courses)}")
        
        # 检查成绩数据
        response = requests.get(f"{BASE_URL}/api/grades")
        grades = response.json()
        print(f"📊 当前成绩数量: {len(grades)}")
        
        # 检查统计信息
        response = requests.get(f"{BASE_URL}/api/statistics/summary")
        stats = response.json()
        print(f"📈 系统统计: {stats}")
        
    except Exception as e:
        print(f"❌ 数据检查失败: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("🎯 学生信息管理系统示例数据初始化")
    print("=" * 60)
    
    # 测试连接
    if not test_connection():
        print("❌ 请确保Flask应用正在运行 (python app.py)")
        return
    
    # 添加数据
    students_added = add_students()
    courses_added = add_courses()
    grades_added = add_grades()
    
    # 检查结果
    check_data()
    
    print("\n" + "=" * 60)
    print("🎉 示例数据初始化完成！")
    print("=" * 60)
    print(f"✅ 学生数据: {students_added}/{len(SAMPLE_STUDENTS)}")
    print(f"✅ 课程数据: {courses_added}/{len(SAMPLE_COURSES)}")
    print(f"✅ 成绩数据: {grades_added}/{len(SAMPLE_GRADES)}")
    print("\n🌐 现在可以访问 http://localhost:5000 查看完整系统！")

if __name__ == "__main__":
    main()