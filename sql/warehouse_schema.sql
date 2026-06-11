-- Week 7 warehouse schema draft

CREATE TABLE IF NOT EXISTS dim_customers (
    customer_key INTEGER PRIMARY KEY,
    customer_id INTEGER,
    full_name VARCHAR(100),
    gender VARCHAR(20),
    preferred_branch_id INTEGER,
    loyalty_points INTEGER
);

CREATE TABLE IF NOT EXISTS dim_services (
    service_key INTEGER PRIMARY KEY,
    service_id INTEGER,
    service_name VARCHAR(100),
    category VARCHAR(50),
    duration_mins INTEGER,
    base_price NUMERIC(10,2)
);

CREATE TABLE IF NOT EXISTS dim_branch (
    branch_key INTEGER PRIMARY KEY,
    branch_id INTEGER,
    branch_name VARCHAR(100),
    city VARCHAR(100),
    status VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE,
    month INTEGER,
    quarter INTEGER,
    year INTEGER
);

CREATE TABLE IF NOT EXISTS fact_sales (
    sales_key INTEGER PRIMARY KEY,
    invoice_id INTEGER,
    customer_key INTEGER,
    service_key INTEGER,
    branch_key INTEGER,
    date_key INTEGER,
    quantity INTEGER,
    gross_amount NUMERIC(10,2),
    discount_amount NUMERIC(10,2),
    tax_amount NUMERIC(10,2),
    net_amount NUMERIC(10,2)
);

CREATE TABLE IF NOT EXISTS fact_bookings (
    booking_key INTEGER PRIMARY KEY,
    appointment_id INTEGER,
    customer_key INTEGER,
    service_key INTEGER,
    branch_key INTEGER,
    date_key INTEGER,
    booking_status VARCHAR(30),
    booking_channel VARCHAR(30),
    completed_flag BOOLEAN
);
