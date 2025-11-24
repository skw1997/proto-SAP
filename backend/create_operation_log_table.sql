-- 创建操作记录表
CREATE TABLE IF NOT EXISTS purchase_orders.po_records (
    id SERIAL PRIMARY KEY,
    user_email VARCHAR(255) NOT NULL,
    table_name VARCHAR(100) NOT NULL,
    operation VARCHAR(20) NOT NULL, -- 'insert', 'update', 'delete'
    record_data JSONB NOT NULL,
    operation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_po_records_user_email ON purchase_orders.po_records(user_email);
CREATE INDEX IF NOT EXISTS idx_po_records_table_name ON purchase_orders.po_records(table_name);
CREATE INDEX IF NOT EXISTS idx_po_records_operation ON purchase_orders.po_records(operation);
CREATE INDEX IF NOT EXISTS idx_po_records_operation_time ON purchase_orders.po_records(operation_time);