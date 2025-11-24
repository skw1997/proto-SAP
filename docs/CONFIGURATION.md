# 系统配置说明

## 1. 数据库配置

系统使用 `.env` 文件来管理数据库连接配置。请按照以下步骤进行配置：

### 编辑 .env 文件
打开 `.env` 文件，修改以下配置项：

```env
# PostgreSQL数据库配置
DB_HOST=localhost           # 数据库主机地址
DB_PORT=5432               # 数据库端口
DB_USER=postgres           # 数据库用户名
DB_PASSWORD=your_password  # 数据库密码（请修改为实际密码）
DB_NAME=purchase_orders    # 数据库名称
```

### 获取正确的数据库信息

1. **DB_HOST**: 通常是 `localhost` 或 `127.0.0.1`
2. **DB_PORT**: PostgreSQL默认端口是 `5432`
3. **DB_USER**: PostgreSQL默认超级用户是 `postgres`
4. **DB_PASSWORD**: 安装PostgreSQL时设置的密码
5. **DB_NAME**: 要连接的数据库名称

## 2. 如何获取PostgreSQL密码

### Windows系统：
1. 打开命令提示符
2. 运行以下命令连接到PostgreSQL：
   ```bash
   psql -U postgres -d postgres
   ```
3. 如果提示输入密码，说明密码认证已启用
4. 如果没有设置过密码，可以设置一个：
   ```sql
   \password postgres
   ```

### 或者查看pg_hba.conf文件：
1. 找到PostgreSQL安装目录下的 `data/pg_hba.conf` 文件
2. 查看认证方法设置

## 3. 测试配置

修改完 .env 文件后，运行以下命令测试连接：

```bash
python env_db_config.py
```

## 4. 创建数据库

如果数据库不存在，可以使用以下SQL命令创建：

```sql
CREATE DATABASE purchase_orders;
```

然后执行 `database_schema.sql` 文件中的SQL语句创建表结构。

## 5. 运行PDF解析器

配置完成后，可以运行PDF解析器：

```bash
python pdf_parser.py
```