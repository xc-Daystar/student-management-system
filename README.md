# 学生信息管理系统

## 项目简介
基于Flask框架开发的学生信息管理系统，提供学生信息管理、课程管理、成绩管理和统计分析功能。

## 功能特性
- 学生信息CRUD操作
- 课程信息管理
- 成绩录入与查询
- 班级平均分统计
- 响应式Web界面

## 技术栈
- 后端：Python Flask
- 前端：HTML5/CSS3/JavaScript
- 数据库：SQLite
- 数据格式：JSON API

## 安装运行

### 环境要求
- Python 3.7+
- pip包管理器

### 安装步骤
1. 安装依赖包：
```bash
pip install -r requirements.txt
```

2. 运行应用：
```bash
python app.py
```

3. 访问系统：
打开浏览器访问 http://127.0.0.1:5000

## 项目结构
```
项目根目录/
├── app.py              # 主应用文件
├── templates/
│   └── index.html      # 前端界面
├── requirements.txt    # 依赖包列表
├── 需求文档            # 项目需求文档
└── README.md          # 项目说明
```

## API接口说明

### 学生管理
- GET /api/students - 获取所有学生
- POST /api/students - 添加新学生
- GET /api/students/<student_id> - 获取特定学生
- PUT /api/students/<student_id> - 更新学生信息
- DELETE /api/students/<student_id> - 删除学生

### 课程管理
- GET /api/courses - 获取所有课程
- POST /api/courses - 添加新课程

### 成绩管理
- GET /api/grades - 获取所有成绩
- POST /api/grades - 录入成绩

### 统计分析
- GET /api/statistics/class-average - 获取班级平均分

## 使用说明
1. 在"学生管理"标签页添加和管理学生信息
2. 在"课程管理"标签页添加课程信息
3. 在"成绩管理"标签页录入学生成绩
4. 在"统计分析"标签页查看班级平均分统计

## 开发规范
- 代码注释完整
- 模块化设计
- RESTful API设计
- 前端响应式布局