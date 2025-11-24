# PostgreSQL数据库设置指南

## 1. 安装PostgreSQL

如果你还没有安装PostgreSQL，请先下载并安装：
- 官网下载：https://www.postgresql.org/download/
- 推荐版本：PostgreSQL 13或更高版本

## 2. 启动PostgreSQL服务

### Windows系统：
1. 打开"服务"管理器（services.msc）
2. 找到"postgresql-x64-xx"服务
3. 右键点击并选择"启动"

### 或者使用命令行：
```bash
# 启动服务
net start postgresql-x64-13

# 停止服务
net stop postgresql-x64-13
```

## 3. 设置数据库密码

### 方法一：使用psql命令行
1. 打开命令提示符或PowerShell
2. 连接到PostgreSQL：
   ```bash
   psql -U postgres -d postgres
   ```
3. 设置密码：
   ```sql
   \password postgres
   ```
4. 输入新密码并确认

### 方法二：修改pg_hba.conf文件
1. 找到PostgreSQL安装目录下的`pg_hba.conf`文件（通常在`data`文件夹中）
2. 找到以下行：
   ```
   # TYPE  DATABASE        USER            ADDRESS                 METHOD
   host    all             all             127.0.0.1/32            md5
   ```
3. 将`md5`改为`trust`（仅用于开发环境，生产环境请保持为`md5`）：
   ```
   host    all             all             127.0.0.1/32            trust
   ```
4. 重启PostgreSQL服务

## 4. 创建数据库和表

### 创建数据库：
```sql
CREATE DATABASE purchase_orders;
```

### 执行表结构脚本：
1. 打开`database_schema.sql`文件
2. 复制所有内容
3. 在psql中执行或使用以下命令：
   ```bash
   psql -U postgres -d purchase_orders -f database_schema.sql
   ```

## 5. 验证配置

运行测试脚本验证连接：
```bash
python test_db_connection.py
```

## 6. 常见问题解决

### 密码认证失败：
1. 确保输入的密码正确
2. 检查pg_hba.conf文件中的认证方法
3. 重启PostgreSQL服务

### 连接被拒绝：
1. 确保PostgreSQL服务正在运行
2. 检查端口号是否正确（默认5432）
3. 检查防火墙设置

### 数据库不存在：
1. 使用`CREATE DATABASE purchase_orders;`创建数据库
2. 确保在连接字符串中使用正确的数据库名称