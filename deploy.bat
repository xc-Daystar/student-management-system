@echo off
REM 学生信息管理系统部署脚本 (Windows版本)

echo === 学生信息管理系统部署脚本 ===

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python3.7+
    pause
    exit /b 1
)

REM 检查依赖
if not exist "requirements.txt" (
    echo 错误: 未找到requirements.txt文件
    pause
    exit /b 1
)

REM 安装依赖
echo 正在安装Python依赖...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

REM 初始化数据库
echo 正在初始化数据库...
python -c "from app import init_db; init_db(); print('数据库初始化完成')"

REM 设置环境变量
if not exist ".env" (
    echo 正在创建环境配置文件...
    copy .env.example .env
    echo 请编辑 .env 文件配置数据库连接等信息
)

REM 启动应用
echo 正在启动学生信息管理系统...
echo 访问地址: http://localhost:5000
echo 按 Ctrl+C 停止服务

python run.py