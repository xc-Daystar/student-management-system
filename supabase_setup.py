#!/usr/bin/env python3
"""
Supabase数据库初始化脚本
用于在Supabase中创建学生信息管理系统的表结构
"""

from supabase import create_client
import os

# Supabase配置
SUPABASE_URL = "https://uuhbirqghkmoqsugjcfh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV1aGJpcnFnaGttb3FzdWdqY2ZoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA1MDkxMzUsImV4cCI6MjA3NjA4NTEzNX0.vDvWe84JPFkN493mEBNv9B6wsda4bkmSGiODntmYRPk"

def init_supabase_tables():
    """初始化Supabase表结构"""
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        print("正在检查Supabase表结构...")
        
        # 检查学生表是否存在，如果不存在则创建
        try:
            response = supabase.table('students').select('*').limit(1).execute()
            print("✓ 学生表已存在")
        except Exception:
            print("⚠ 学生表不存在，请在Supabase控制台手动创建表")
            print("建议的表结构：")
            print("""
            CREATE TABLE students (
                id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                student_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                gender TEXT NOT NULL,
                age INTEGER NOT NULL,
                class_name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                address TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """)
        
        # 检查课程表
        try:
            response = supabase.table('courses').select('*').limit(1).execute()
            print("✓ 课程表已存在")
        except Exception:
            print("⚠ 课程表不存在，请在Supabase控制台手动创建表")
            print("建议的表结构：")
            print("""
            CREATE TABLE courses (
                id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                course_code TEXT UNIQUE NOT NULL,
                course_name TEXT NOT NULL,
                teacher TEXT NOT NULL,
                credit INTEGER NOT NULL,
                semester TEXT,
                description TEXT
            );
            """)
        
        # 检查成绩表
        try:
            response = supabase.table('grades').select('*').limit(1).execute()
            print("✓ 成绩表已存在")
        except Exception:
            print("⚠ 成绩表不存在，请在Supabase控制台手动创建表")
            print("建议的表结构：")
            print("""
            CREATE TABLE grades (
                id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                student_id TEXT NOT NULL,
                course_code TEXT NOT NULL,
                score REAL NOT NULL,
                semester TEXT NOT NULL,
                exam_date DATE,
                remarks TEXT,
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (course_code) REFERENCES courses(course_code)
            );
            """)
        
        print("\nSupabase表结构检查完成！")
        print("如果表不存在，请在Supabase控制台的SQL编辑器中执行上述SQL语句创建表")
        
    except Exception as e:
        print(f"Supabase连接失败: {e}")

if __name__ == '__main__':
    init_supabase_tables()