-- PostgreSQL Database Dump
-- Project: AssetFlow Management System (Industrial Grade)

-- 1. Table for Categories (To organize items efficiently)
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    description TEXT
);

-- 2. Table for Employees (Handles the 1000+ employee requirement)
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    emp_id VARCHAR(20) UNIQUE NOT NULL, -- Unique HR reference
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    department VARCHAR(100),
    designation VARCHAR(100)
);

-- 3. Table for Assets (Hardware/Software Inventory)
CREATE TABLE assets (
    id SERIAL PRIMARY KEY,
    asset_tag_id VARCHAR(50) UNIQUE NOT NULL, -- Barcode/Tag ID
    category_id INTEGER, -- Simple ID reference (No hard constraint)
    brand VARCHAR(100),
    model VARCHAR(100),
    serial_number VARCHAR(255),
    status VARCHAR(50) DEFAULT 'In Stock'
);

-- 4. Table for Assignments (Tracking the flow of items)
CREATE TABLE assignments (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER,    -- Simple ID reference
    employee_id INTEGER, -- Simple ID reference
    issue_date DATE DEFAULT CURRENT_DATE,
    return_date DATE,
    remarks TEXT
);

-- INSERTING DUMMY DATA (Required for testing)
INSERT INTO categories (category_name, description) VALUES 
('Laptops', 'Corporate standard workstations'),
('Peripherals', 'External monitors and keyboards');

INSERT INTO employees (emp_id, full_name, email, department, designation) VALUES 
('EMP001', 'Neha Sharma', 'neha.s@company.com', 'Engineering', 'Developer'),
('EMP002', 'Aravind Kumar', 'aravind.k@company.com', 'HR', 'HR Specialist');

INSERT INTO assets (asset_tag_id, category_id, brand, model, status) VALUES 
('ASSET-2026-001', 1, 'Dell', 'Latitude 5420', 'Assigned'),
('ASSET-2026-002', 1, 'Apple', 'MacBook Air', 'In Stock');

INSERT INTO assignments (asset_id, employee_id, remarks) VALUES 
(1, 1, 'Issued with laptop bag and charger');