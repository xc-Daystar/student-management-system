-- Supabase学生信息管理系统表结构创建脚本
-- 请在Supabase控制台的SQL编辑器中执行此脚本

-- 创建学生表
CREATE TABLE IF NOT EXISTS students (
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

-- 创建课程表
CREATE TABLE IF NOT EXISTS courses (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    course_code TEXT UNIQUE NOT NULL,
    course_name TEXT NOT NULL,
    teacher TEXT NOT NULL,
    credit INTEGER NOT NULL,
    semester TEXT,
    description TEXT
);

-- 创建成绩表
CREATE TABLE IF NOT EXISTS grades (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    student_id TEXT NOT NULL,
    course_code TEXT NOT NULL,
    score REAL NOT NULL,
    semester TEXT NOT NULL,
    exam_date DATE,
    remarks TEXT
);

-- 插入示例数据
INSERT INTO students (student_id, name, gender, age, class_name, email, phone, address) VALUES
('2023001', '张三', '男', 20, '计算机科学与技术1班', 'zhangsan@example.com', '13800138001', '北京市海淀区'),
('2023002', '李四', '女', 19, '计算机科学与技术1班', 'lisi@example.com', '13800138002', '北京市朝阳区'),
('2023003', '王五', '男', 21, '软件工程2班', 'wangwu@example.com', '13800138003', '北京市西城区');

INSERT INTO courses (course_code, course_name, teacher, credit, semester, description) VALUES
('CS101', '计算机基础', '张教授', 3, '2023-秋季', '计算机科学基础课程'),
('CS201', '数据结构', '李教授', 4, '2023-秋季', '数据结构与算法课程'),
('CS301', '数据库系统', '王教授', 3, '2024-春季', '数据库原理与应用');

INSERT INTO grades (student_id, course_code, score, semester, exam_date, remarks) VALUES
('2023001', 'CS101', 85.5, '2023-秋季', '2023-12-20', '良好'),
('2023001', 'CS201', 92.0, '2023-秋季', '2023-12-25', '优秀'),
('2023002', 'CS101', 78.0, '2023-秋季', '2023-12-20', '及格'),
('2023003', 'CS301', 88.5, '2024-春季', '2024-06-15', '良好');

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_students_class_name ON students(class_name);
CREATE INDEX IF NOT EXISTS idx_grades_student_id ON grades(student_id);
CREATE INDEX IF NOT EXISTS idx_grades_course_code ON grades(course_code);
CREATE INDEX IF NOT EXISTS idx_grades_semester ON grades(semester);

-- 启用行级安全策略（可选）
ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE grades ENABLE ROW LEVEL SECURITY;

-- 创建允许所有操作的策略（开发环境）
CREATE POLICY "允许所有操作" ON students FOR ALL USING (true);
CREATE POLICY "允许所有操作" ON courses FOR ALL USING (true);
CREATE POLICY "允许所有操作" ON grades FOR ALL USING (true);

-- 查看表结构
COMMENT ON TABLE students IS '学生信息表';
COMMENT ON TABLE courses IS '课程信息表';
COMMENT ON TABLE grades IS '学生成绩表';