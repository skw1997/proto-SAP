# SAP-like 采购订单管理系统

这是一个基于Python和PostgreSQL的采购订单管理系统，支持PDF采购订单的自动解析和导入到数据库中。

## 功能特性

1. **多公司PDF支持**：支持不同格式的采购订单PDF文件解析
2. **自动数据提取**：从PDF中自动提取关键信息并映射到数据库字段
3. **数据验证**：验证数量×单价=总价的正确性
4. **Web界面管理**：提供友好的Web界面进行数据浏览和管理
5. **公司配置管理**：支持添加新的公司映射配置
6. **文件上传管理**：支持拖拽上传和多文件选择
7. **数据库表管理**：支持四种不同状态的采购订单表（WF Open/Closed, Non-WF Open/Closed）
8. **操作日志记录**：记录所有用户操作（新增、修改、删除）到操作日志表

## 系统架构

```
SAP_like/
├── backend/              # 后端服务
│   ├── controllers/       # 控制器层
│   ├── models/           # 数据模型层
│   ├── routes/           # 路由配置
│   ├── utils/            # 工具函数
│   ├── app.py            # Flask应用入口
│   ├── web_app.py        # Web应用配置
│   ├── db_connection.py  # 数据库连接
│   ├── db_pdf_processor.py # PDF数据处理
│   ├── pdf_import_processor.py # PDF导入处理器
│   ├── pdf_import_ui.py  # PDF导入界面
│   ├── operation_logger.py # 操作日志记录器
│   ├── init_operation_log_table.py # 操作日志表初始化脚本
│   └── enhanced_db_manager.py # 增强数据库管理器
├── frontend/             # 前端页面
├── config/               # 配置文件
├── uploads/              # 上传文件目录
├── pdf_samples/          # PDF示例文件
└── utils/                # 实用工具脚本

## 操作日志表结构

系统会自动创建 `po_records` 表来记录所有用户操作：

- `id`: 自增主键
- `user_email`: 用户邮箱
- `table_name`: 操作的表名
- `operation`: 操作类型（insert/update/delete）
- `record_data`: 完整的记录数据（JSON格式）
- `operation_time`: 操作时间

## API端点

除了原有的API端点外，新增了以下端点用于操作日志：

- `GET /api/operation_logs` - 获取操作日志（支持过滤参数：user_email, table_name, operation, limit）

## 使用说明

1. 确保已安装所有依赖：`pip install -r requirements.txt`
2. 配置数据库连接信息到 `.env` 文件
3. 初始化数据库结构：`python utils/update_database_structure.py`
4. 启动后端服务：`python backend/app.py`
5. 访问Web界面：http://localhost:5000