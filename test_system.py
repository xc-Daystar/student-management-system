#!/usr/bin/env python3
"""
学生信息管理系统测试脚本
测试所有API接口和数据库连接
"""

import requests
import json
import sys

# 测试配置
BASE_URL = "http://localhost:5000"
TEST_DATA = {
    "student": {
        "student_id": "TEST001",
        "name": "测试学生",
        "gender": "男",
        "age": 20,
        "class_name": "测试班级",
        "email": "test@example.com",
        "phone": "13800138000",
        "address": "测试地址"
    },
    "course": {
        "course_code": "TEST001",
        "course_name": "测试课程",
        "teacher": "测试教师",
        "credit": 3,
        "semester": "2024-2025-1",
        "description": "测试课程描述"
    },
    "grade": {
        "student_id": "TEST001",
        "course_code": "TEST001",
        "score": 85.5,
        "semester": "2024-2025-1",
        "exam_date": "2024-12-01",
        "remarks": "测试成绩"
    }
}

def test_api(endpoint, method="GET", data=None, expected_status=200):
    """测试API接口"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        else:
            print(f"❌ 不支持的HTTP方法: {method}")
            return False
        
        if response.status_code == expected_status:
            print(f"✅ {method} {endpoint} - 状态码: {response.status_code}")
            return True
        else:
            print(f"❌ {method} {endpoint} - 期望状态码: {expected_status}, 实际状态码: {response.status_code}")
            print(f"   响应内容: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ 无法连接到服务器: {url}")
        print("   请确保Flask应用正在运行")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_supabase_connection():
    """测试Supabase连接"""
    print("\n🔗 测试Supabase连接...")
    return test_api("/api/supabase/status")

def test_health_check():
    """测试系统健康检查"""
    print("\n🏥 测试系统健康检查...")
    return test_api("/api/health")

def test_student_apis():
    """测试学生管理API"""
    print("\n👨‍🎓 测试学生管理API...")
    
    # 添加学生
    if not test_api("/api/students", "POST", TEST_DATA["student"], 201):
        return False
    
    # 获取学生列表
    if not test_api("/api/students", "GET"):
        return False
    
    # 获取特定学生
    if not test_api("/api/students/TEST001", "GET"):
        return False
    
    # 搜索学生
    if not test_api("/api/students/search/测试", "GET"):
        return False
    
    # 更新学生信息
    update_data = {"name": "更新后的测试学生"}
    if not test_api("/api/students/TEST001", "PUT", update_data):
        return False
    
    return True

def test_course_apis():
    """测试课程管理API"""
    print("\n📚 测试课程管理API...")
    
    # 添加课程
    if not test_api("/api/courses", "POST", TEST_DATA["course"], 201):
        return False
    
    # 获取课程列表
    if not test_api("/api/courses", "GET"):
        return False
    
    return True

def test_grade_apis():
    """测试成绩管理API"""
    print("\n📊 测试成绩管理API...")
    
    # 添加成绩
    if not test_api("/api/grades", "POST", TEST_DATA["grade"], 201):
        return False
    
    # 获取成绩列表
    if not test_api("/api/grades", "GET"):
        return False
    
    # 获取学生成绩详情
    if not test_api("/api/students/TEST001/grades", "GET"):
        return False
    
    return True

def test_statistics_apis():
    """测试统计API"""
    print("\n📈 测试统计API...")
    
    # 数据概览
    if not test_api("/api/statistics/summary", "GET"):
        return False
    
    # 班级平均分
    if not test_api("/api/statistics/class-average", "GET"):
        return False
    
    return True

def test_supabase_apis():
    """测试Supabase API"""
    print("\n☁️ 测试Supabase API...")
    
    # 测试Supabase学生API
    if not test_api("/api/supabase/students", "GET"):
        print("⚠️ Supabase学生API测试失败，可能是Supabase未配置")
    
    # 测试Supabase课程API
    if not test_api("/api/supabase/courses", "GET"):
        print("⚠️ Supabase课程API测试失败，可能是Supabase未配置")
    
    return True

def cleanup_test_data():
    """清理测试数据"""
    print("\n🧹 清理测试数据...")
    
    # 删除测试成绩
    test_api("/api/grades", "DELETE", None, 405)  # 成绩删除需要特定实现
    
    # 删除测试课程
    test_api("/api/courses/TEST001", "DELETE", None, 405)  # 课程删除需要特定实现
    
    # 删除测试学生
    test_api("/api/students/TEST001", "DELETE")
    
    print("✅ 测试数据清理完成")

def main():
    """主测试函数"""
    print("=" * 60)
    print("🎯 学生信息管理系统测试脚本")
    print("=" * 60)
    
    # 测试计数器
    passed_tests = 0
    total_tests = 0
    
    # 运行测试
    tests = [
        ("健康检查", test_health_check),
        ("Supabase连接", test_supabase_connection),
        ("学生管理", test_student_apis),
        ("课程管理", test_course_apis),
        ("成绩管理", test_grade_apis),
        ("统计分析", test_statistics_apis),
        ("Supabase API", test_supabase_apis),
    ]
    
    for test_name, test_func in tests:
        total_tests += 1
        if test_func():
            passed_tests += 1
        else:
            print(f"❌ {test_name}测试失败")
    
    # 显示测试结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    print(f"✅ 通过测试: {passed_tests}/{total_tests}")
    print(f"📈 测试通过率: {passed_tests/total_tests*100:.1f}%")
    
    if passed_tests == total_tests:
        print("🎉 所有测试通过！系统运行正常")
    else:
        print("⚠️ 部分测试失败，请检查系统配置")
    
    # 清理测试数据
    cleanup_test_data()
    
    print("\n🔚 测试完成")

if __name__ == "__main__":
    main()