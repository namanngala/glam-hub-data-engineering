-- Analyst-friendly warehouse views

CREATE OR REPLACE VIEW vw_fact_sales_enriched AS
SELECT
    fs.sales_key,
    dc.full_name AS customer_name,
    ds.service_name,
    db.branch_name,
    dd.full_date,
    fs.net_amount
FROM fact_sales fs
LEFT JOIN dim_customers dc
    ON fs.customer_key = dc.customer_key
LEFT JOIN dim_services ds
    ON fs.service_key = ds.service_key
LEFT JOIN dim_branch db
    ON fs.branch_key = db.branch_key
LEFT JOIN dim_date dd
    ON fs.date_key = dd.date_key;

CREATE OR REPLACE VIEW vw_fact_bookings_enriched AS
SELECT
    fb.booking_key,
    dc.full_name AS customer_name,
    ds.service_name,
    db.branch_name,
    dd.full_date,
    fb.booking_status,
    fb.booking_channel,
    fb.completed_flag
FROM fact_bookings fb
LEFT JOIN dim_customers dc
    ON fb.customer_key = dc.customer_key
LEFT JOIN dim_services ds
    ON fb.service_key = ds.service_key
LEFT JOIN dim_branch db
    ON fb.branch_key = db.branch_key
LEFT JOIN dim_date dd
    ON fb.date_key = dd.date_key;
