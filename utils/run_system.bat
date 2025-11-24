@echo off
echo PostgreSQL PDF采购订单解析系统
echo ===============================

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 检查依赖包
echo 检查依赖包...
python -c "import psycopg2, PyPDF2, dotenv" >nul 2>&1
if %errorlevel% neq 0 (
    echo 安装依赖包...
    pip install psycopg2-binary PyPDF2 python-dotenv >nul 2>&1
    if %errorlevel% neq 0 (
        echo 错误: 无法安装依赖包
        pause
        exit /b 1
    )
)

REM 测试数据库连接
echo 测试数据库连接...
python test_db_connection.py
if %errorlevel% neq 0 (
    echo 警告: 数据库连接测试失败，请检查配置
    echo 请参考 CONFIGURATION.md 和 DATABASE_SETUP.md 文件
    pause
    REM 继续执行，因为用户可能想先看配置说明
)

echo.
echo 系统已准备就绪!
echo.
echo 使用方法:
echo 1. 编辑 .env 文件配置数据库连接信息
echo 2. 运行 python pdf_parser.py 解析PDF文件
echo 3. 运行 python advanced_pdf_parser.py 使用高级解析器
echo.
echo 按任意键退出...
pause >nul