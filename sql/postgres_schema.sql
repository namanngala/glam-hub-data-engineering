-- Glam Hub operational schema (lightweight draft)
CREATE TABLE IF NOT EXISTS branches (
    branch_id INTEGER PRIMARY KEY,
    branch_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    address VARCHAR(200),
    city VARCHAR(100),
    status VARCHAR(20),
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    preferred_branch_id INTEGER REFERENCES branches(branch_id),
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(120),
    gender VARCHAR(20),
    loyalty_points INTEGER DEFAULT 0,
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staff (
    staff_id INTEGER PRIMARY KEY,
    branch_id INTEGER REFERENCES branches(branch_id),
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(50),
    specialization VARCHAR(50),
    phone VARCHAR(20),
    hire_date DATE,
    is_active BOOLEAN
);

CREATE TABLE IF NOT EXISTS services (
    service_id INTEGER PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    duration_mins INTEGER,
    base_price NUMERIC(10,2),
    is_active BOOLEAN
);

CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    branch_id INTEGER REFERENCES branches(branch_id),
    product_name VARCHAR(100) NOT NULL,
    sku_code VARCHAR(50),
    category VARCHAR(50),
    unit_price NUMERIC(10,2),
    stock_qty INTEGER,
    reorder_threshold INTEGER
);

CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INTEGER PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    branch_id INTEGER REFERENCES branches(branch_id),
    staff_id INTEGER REFERENCES staff(staff_id),
    primary_service_id INTEGER REFERENCES services(service_id),
    appointment_datetime TIMESTAMP,
    status VARCHAR(30),
    booking_channel VARCHAR(30),
    checked_in_at TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS invoices (
    invoice_id INTEGER PRIMARY KEY,
    appointment_id INTEGER REFERENCES appointments(appointment_id),
    customer_id INTEGER REFERENCES customers(customer_id),
    invoice_date DATE,
    subtotal NUMERIC(10,2),
    tax_amount NUMERIC(10,2),
    discount_amount NUMERIC(10,2),
    total_amount NUMERIC(10,2),
    invoice_status VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS invoice_items (
    invoice_item_id INTEGER PRIMARY KEY,
    invoice_id INTEGER REFERENCES invoices(invoice_id),
    service_id INTEGER REFERENCES services(service_id),
    product_id INTEGER REFERENCES products(product_id),
    item_type VARCHAR(20),
    quantity INTEGER,
    unit_price NUMERIC(10,2),
    line_total NUMERIC(10,2)
);

CREATE TABLE IF NOT EXISTS analytics_appointments (
    appointment_id INTEGER,
    customer_id INTEGER,
    full_name VARCHAR(100),
    branch_name VARCHAR(100),
    staff_name VARCHAR(100),
    service_name VARCHAR(100),
    category VARCHAR(50),
    appointment_datetime TIMESTAMP,
    status VARCHAR(30),
    booking_channel VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS analytics_invoice_summary (
    invoice_id INTEGER,
    appointment_id INTEGER,
    customer_id INTEGER,
    full_name VARCHAR(100),
    branch_name VARCHAR(100),
    service_name VARCHAR(100),
    category VARCHAR(50),
    invoice_date DATE,
    subtotal NUMERIC(10,2),
    tax_amount NUMERIC(10,2),
    discount_amount NUMERIC(10,2),
    total_amount NUMERIC(10,2),
    invoice_status VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS analytics_service_revenue (
    service_id INTEGER,
    service_name VARCHAR(100),
    total_quantity INTEGER,
    total_revenue NUMERIC(12,2)
);
