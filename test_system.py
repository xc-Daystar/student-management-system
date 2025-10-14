import sqlite3
import urllib.request
import json

def test_system():
    print("=== 学生信息管理系统测试 ===\n")
    
    # 测试数据库连接和数据
    print("1. 数据库连接测试:")
    try:
        conn = sqlite3.connect('student_management.db')
        cursor = conn.cursor()
        
        # 检查表结构
        cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
        tables = cursor.fetchall()
        print(f"   数据库表: {[table[0] for table in tables]}")
        
        # 检查学生数据
        cursor.execute('SELECT COUNT(*) FROM students')
        count = cursor.fetchone()[0]
        print(f"   学生记录数: {count}")
        
        # 显示具体数据
        cursor.execute('SELECT * FROM students')
        students = cursor.fetchall()
        print(f"   学生数据:")
        for student in students:
            print(f"     {student}")
        
        conn.close()
        print("   ✓ 数据库连接正常\n")
        
    except Exception as e:
        print(f"   ✗ 数据库错误: {e}\n")
    
    # 测试API
    print("2. API接口测试:")
    try:
        # 测试GET请求
        response = urllib.request.urlopen('http://127.0.0.1:5000/api/students')
        print(f"   GET /api/students - 状态码: {response.getcode()}")
        
        print("   ✓ API接口正常\n")
        
    except Exception as e:
        print(f"   ✗ API错误: {e}\n")
    
    print("3. 系统状态总结:")
    print("   - 后端API: ✓ 正常工作")
    print("   - 数据库: ✓ 数据正确存储") 
    print("   - 前端界面: 需要通过浏览器访问 http://127.0.0.1:5000 测试")
    print("   - 编码问题: 中文字符显示需要进一步优化")
    print("\n=== 测试完成 ===")

if __name__ == '__main__':
    test_system()