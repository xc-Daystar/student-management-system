import sqlite3

def check_database():
    try:
        # 连接数据库
        conn = sqlite3.connect('student_management.db')
        cursor = conn.cursor()
        
        # 检查所有表
        cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
        tables = cursor.fetchall()
        print('数据库中的表:')
        for table in tables:
            print(f'- {table[0]}')
        
        # 检查学生表结构
        print('\n学生表结构:')
        cursor.execute('PRAGMA table_info(students)')
        for col in cursor.fetchall():
            print(f'列 {col[0]}: {col[1]} ({col[2]})')
        
        # 检查学生数据
        print('\n学生表中的数据:')
        cursor.execute('SELECT * FROM students')
        students = cursor.fetchall()
        if students:
            for student in students:
                print(student)
        else:
            print('学生表为空')
        
        conn.close()
        print('\n数据库检查完成')
        
    except Exception as e:
        print(f'检查数据库时出错: {e}')

if __name__ == '__main__':
    check_database()