# PDF采购订单解析系统使用说明

## 系统功能

该系统可以自动解析两种格式的PDF采购订单文件，并将数据导入到PostgreSQL数据库中：

1. **WeFabricate PDF格式** - 导入到 `wf_open` 表
2. **Centurion PDF格式** - 导入到 `non_wf_open` 表

## 系统要求

- Python 3.6+
- PostgreSQL数据库
- 安装依赖包：`pip install -r requirements.txt`

## 安装和配置

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置数据库连接
编辑 `.env` 文件，填入正确的数据库连接信息：
```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=purchase_orders
```

### 3. 创建数据库和表
```bash
python create_database.py
```

## 使用方法

### 方法一：使用主解析器
```bash
python pdf_parser.py
```

### 方法二：使用高级解析器
```bash
python advanced_pdf_parser.py
```

### 方法三：使用测试脚本
```bash
python final_test.py
```

## 系统架构

### 主要文件说明

- `pdf_parser.py` - 基础PDF解析器
- `advanced_pdf_parser.py` - 增强版PDF解析器
- `column_mapping.json` - PDF解析配置文件
- `database_schema.sql` - 数据库表结构定义
- `create_database.py` - 数据库创建脚本
- `test_db_connection.py` - 数据库连接测试
- `check_data.py` - 数据检查脚本

### 数据库表结构

#### WF Open 表 (wf_open)
存储WeFabricate采购订单数据

#### Non-WF Open 表 (non_wf_open)
存储Centurion采购订单数据

## 扩展支持

### 添加新的PDF格式支持

1. 在 `column_mapping.json` 中添加新的配置项
2. 在解析器类中添加相应的解析方法
3. 根据需要调整正则表达式模式

### 自定义数据库表

如果需要修改数据库表结构，请同时更新：
1. `database_schema.sql`
2. 解析器中的数据库插入代码
3. 相关的配置映射

## 常见问题

### 1. 数据库连接失败
- 检查PostgreSQL服务是否正在运行
- 验证 `.env` 文件中的连接信息是否正确
- 确认PostgreSQL密码是否正确

### 2. PDF解析结果为空
- 检查PDF文件格式是否与配置匹配
- 查看 `detailed_debug.py` 脚本的输出结果
- 调整 `column_mapping.json` 中的正则表达式

### 3. 数据插入失败
- 检查数据库表结构是否正确创建
- 确认数据库用户是否有写入权限
- 查看错误日志获取详细信息

## 维护和更新

### 更新解析规则
编辑 `column_mapping.json` 文件来调整PDF解析规则

### 更新数据库结构
修改 `database_schema.sql` 文件并重新运行 `create_database.py`

## 技术支持

如遇到问题，请检查：
1. 所有依赖包是否正确安装
2. 数据库连接是否正常
3. PDF文件格式是否符合预期
4. 配置文件是否正确设置