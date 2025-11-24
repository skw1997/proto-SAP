-- 创建Schema
CREATE SCHEMA IF NOT EXISTS purchase_orders;

-- 使用Schema
SET search_path TO purchase_orders;

-- WF Open 表
CREATE TABLE wf_open (
    po VARCHAR(50),
    pn VARCHAR(50) PRIMARY KEY,
    line INTEGER,
    po_line VARCHAR(50),
    description TEXT,
    qty DECIMAL(10, 2),
    net_price DECIMAL(10, 2),
    total_price DECIMAL(10, 2),
    req_date_wf DATE,
    eta_wfsz DATE,
    shipping_mode VARCHAR(50),
    comment TEXT,
    po_placed_date DATE,
    purchaser VARCHAR(100),
    record_no VARCHAR(50),
    shipping_cost DECIMAL(10, 2),
    tracking_no VARCHAR(100),
    so_number VARCHAR(50),
    latest_departure_date DATE
);

-- 为po_line字段添加唯一约束
ALTER TABLE wf_open ADD CONSTRAINT uk_wf_open_po_line UNIQUE (po_line);

-- WF Closed 表
CREATE TABLE wf_closed (
    id SERIAL PRIMARY KEY,
    po VARCHAR(50),
    pn VARCHAR(50),
    line INTEGER,
    pn_line VARCHAR(50),
    description TEXT,
    qty DECIMAL(10, 2),
    net_price DECIMAL(10, 2),
    total_price DECIMAL(10, 2),
    req_date_wf DATE,
    eta_wfsz DATE,
    shipping_mode VARCHAR(50),
    comment TEXT,
    po_placed_date DATE,
    purchaser VARCHAR(100),
    record_no VARCHAR(50),
    shipping_cost DECIMAL(10, 2),
    tracking_no VARCHAR(100),
    so_number VARCHAR(50),
    chinese_name VARCHAR(100),
    unit VARCHAR(20)
);

-- Non-WF Open 表
CREATE TABLE non_wf_open (
    po VARCHAR(50),
    pn VARCHAR(50) PRIMARY KEY,
    description TEXT,
    qty DECIMAL(10, 2),
    net_price DECIMAL(10, 2),
    total_price DECIMAL(10, 2),
    req_date DATE,
    eta_wfsz DATE,
    shipping_mode VARCHAR(50),
    comment TEXT,
    po_placed_date DATE,
    qc_result VARCHAR(50),
    shipping_cost DECIMAL(10, 2),
    tracking_no VARCHAR(100),
    so_number VARCHAR(50),
    yes_not_paid VARCHAR(10)
);

-- Non-WF Closed 表
CREATE TABLE non_wf_closed (
    id SERIAL PRIMARY KEY,
    po VARCHAR(50),
    pn VARCHAR(50),
    description TEXT,
    qty DECIMAL(10, 2),
    net_price DECIMAL(10, 2),
    total_price DECIMAL(10, 2),
    req_date DATE,
    eta_wfsz DATE,
    shipping_mode VARCHAR(50),
    comment TEXT,
    po_placed_date DATE,
    purchaser VARCHAR(100),
    shipping_cost DECIMAL(10, 2),
    tracking_no VARCHAR(100),
    so_number VARCHAR(50),
    yes_not_paid VARCHAR(10)
);