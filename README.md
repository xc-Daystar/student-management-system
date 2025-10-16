# 学生信息管理系统

一个基于Flask框架的学生信息管理系统，支持SQLite本地数据库和Supabase云数据库。

## 功能特性

### 核心功能
- **学生管理**: 添加、编辑、删除、搜索学生信息
- **课程管理**: 管理课程信息和授课教师
- **成绩管理**: 录入和查询学生成绩
- **统计分析**: 班级平均分统计和系统数据概览

### 数据库支持
- **SQLite**: 本地数据库，适合单机使用
- **Supabase**: 云数据库，支持多设备同步访问

### 技术栈
- **后端**: Flask + SQLAlchemy
- **前端**: HTML5 + CSS3 + JavaScript
- **数据库**: SQLite / Supabase (PostgreSQL)
- **部署**: 支持本地部署和Vercel云部署

## 快速开始

### 环境要求
- Python 3.7+
- pip包管理器

### 安装步骤

1. **克隆项目**
```bash
git clone <项目地址>
cd 251014
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **初始化数据库**
```bash
python app.py
```

4. **访问系统**
打开浏览器访问: http://localhost:5000

### Supabase配置（可选）

如果需要使用Supabase云数据库：

1. 在Supabase官网创建项目
2. 获取项目URL和API密钥
3. 在app.py中配置Supabase连接信息
4. 运行Supabase初始化脚本：
```bash
python supabase_setup.py
```

## API接口文档

### 学生管理接口
- `GET /api/students` - 获取所有学生
- `POST /api/students` - 添加新学生
- `GET /api/students/<student_id>` - 获取特定学生
- `PUT /api/students/<student_id>` - 更新学生信息
- `DELETE /api/students/<student_id>` - 删除学生
- `GET /api/students/search/<keyword>` - 搜索学生

### 课程管理接口
- `GET /api/courses` - 获取所有课程
- `POST /api/courses` - 添加新课程

### 成绩管理接口
- `GET /api/grades` - 获取所有成绩
- `POST /api/grades` - 录入成绩
- `GET /api/students/<student_id>/grades` - 获取学生成绩详情

### 统计接口
- `GET /api/statistics/summary` - 系统数据概览
- `GET /api/statistics/class-average` - 班级平均分统计

### Supabase接口
- `GET /api/supabase/status` - Supabase连接状态检查
- `GET/POST /api/supabase/students` - Supabase学生管理
- `GET/POST /api/supabase/courses` - Supabase课程管理
- `GET/POST /api/supabase/grades` - Supabase成绩管理

## 数据库结构

### 学生表 (students)
- student_id (主键): 学号
- name: 姓名
- gender: 性别
- age: 年龄
- class_name: 班级
- email: 邮箱
- phone: 电话
- address: 地址
- created_at: 创建时间

### 课程表 (courses)
- course_code (主键): 课程代码
- course_name: 课程名称
- teacher: 授课教师
- credit: 学分
- semester: 学期
- description: 课程描述

### 成绩表 (grades)
- id (主键): 成绩ID
- student_id: 学生学号
- course_code: 课程代码
- score: 成绩
- semester: 学期
- exam_date: 考试日期
- remarks: 备注

## 部署说明

### 本地部署
```bash
python app.py
```

### Vercel部署
1. 在Vercel平台导入项目
2. 配置环境变量（如需使用Supabase）
3. 部署完成

### 环境变量配置
```bash
# Supabase配置
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Flask配置
FLASK_ENV=production
```

## 使用指南

### 学生管理
1. 在"学生管理"标签页填写学生信息
2. 点击"添加学生"按钮提交
3. 使用搜索功能快速查找学生
4. 点击"编辑"或"删除"按钮管理学生

### 课程管理
1. 切换到"课程管理"标签页
2. 填写课程信息并提交
3. 系统自动显示所有课程列表

### 成绩管理
1. 在"成绩管理"标签页录入成绩
2. 选择学生学号和课程代码
3. 输入成绩和学期信息
4. 系统自动关联学生和课程信息

### 统计分析
1. 查看"统计分析"标签页
2. 系统显示班级平均分统计
3. 数据概览显示系统整体情况

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查SQLite数据库文件权限
   - 确认Supabase配置信息正确

2. **前端显示异常**
   - 清除浏览器缓存
   - 检查网络连接

3. **API请求失败**
   - 查看浏览器控制台错误信息
   - 检查后端服务是否正常运行

### 技术支持

如有问题，请检查：
- 系统日志文件
- 浏览器开发者工具
- 网络连接状态

## 版本历史

### v1.0.0 (当前版本)
- 基础学生信息管理功能
- SQLite和Supabase双数据库支持
- 完整的CRUD操作接口
- 响应式前端界面
- 统计分析功能

## 许可证

本项目采用MIT许可证。详见LICENSE文件。

---

**开发团队**: 学生信息管理系统开发组  
**最后更新**: 2025年10月15日  
**版本**: 1.0.0