# PDF采购订单解析和导入系统

该系统用于解析PDF格式的采购订单并将数据导入到PostgreSQL数据库中。

## 文件说明

1. `database_schema.sql` - 数据库表结构定义
2. `db_connection.py` - 数据库连接和基本查询示例
3. `pdf_parser.py` - 基础PDF解析器
4. `advanced_pdf_parser.py` - 增强版PDF解析器（支持货币转换和灵活配置）
5. `column_mapping.json` - 列映射配置文件
6. `requirements.txt` - Python依赖包列表

## 安装依赖

```bash
pip install -r requirements.txt
```

## 数据库设置

1. 执行 `database_schema.sql` 中的SQL语句创建数据库表
2. 修改 `db_connection.py` 和 `pdf_parser.py` 中的数据库配置信息

## 使用方法

### 1. 基础使用
```python
from pdf_parser import PDFParser

# 配置数据库连接
db_config = {
    'host': 'localhost',
    'database': 'your_database_name',
    'user': 'your_username',
    'password': 'your_password',
    'port': '5432'
}

parser = PDFParser(db_config)

# 解析PDF并导入数据
wf_data = parser.parse_wefabricate_pdf("Purchase Order - 4500010647.pdf")
parser.insert_wf_open_data(wf_data)
```

### 2. 高级使用
```python
from advanced_pdf_parser import AdvancedPDFParser

parser = AdvancedPDFParser(db_config)

# 解析PDF并导入数据
non_wf_data = parser.parse_centurion_pdf("Centurion Safety Products Purchase Order PO-100130.pdf")
parser.insert_non_wf_open_data(non_wf_data)
```

## 配置文件说明

`column_mapping.json` 文件用于配置不同供应商PDF的解析规则：

- `pdf_patterns`: PDF中关键信息的正则表达式模式
- `table_columns`: 表格列标题的名称
- `database_mapping`: PDF列与数据库列的映射关系
- `currency_mapping`: 货币代码与符号的映射
- `date_formats`: 支持的日期格式列表

## 扩展支持

要添加新的供应商或PDF格式支持：

1. 在 `column_mapping.json` 中添加新的配置项
2. 在解析器类中添加相应的解析方法
3. 根据需要调整正则表达式模式

## 注意事项

1. 确保PDF文件格式与配置文件中的模式匹配
2. 货币转换功能目前简化处理，实际使用中可能需要集成汇率API
3. 日期解析支持多种格式，可根据需要添加更多格式