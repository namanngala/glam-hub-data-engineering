-- Reporting / analytics views

CREATE OR REPLACE VIEW vw_daily_revenue AS
SELECT
    invoice_date,
    COUNT(*) AS invoice_count,
    SUM(total_amount) AS total_revenue
FROM analytics_invoice_summary
GROUP BY invoice_date
ORDER BY invoice_date;

CREATE OR REPLACE VIEW vw_branch_revenue AS
SELECT
    branch_name,
    COUNT(*) AS invoice_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_invoice_value
FROM analytics_invoice_summary
GROUP BY branch_name
ORDER BY total_revenue DESC;

CREATE OR REPLACE VIEW vw_appointment_status_summary AS
SELECT
    branch_name,
    status,
    COUNT(*) AS appointment_count
FROM analytics_appointments
GROUP BY branch_name, status
ORDER BY branch_name, appointment_count DESC;

CREATE OR REPLACE VIEW vw_service_revenue AS
SELECT
    service_name,
    total_quantity,
    total_revenue
FROM analytics_service_revenue
ORDER BY total_revenue DESC;

CREATE OR REPLACE VIEW vw_customer_visit_summary AS
SELECT
    customer_id,
    full_name,
    COUNT(*) AS total_appointments,
    SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed_appointments
FROM analytics_appointments
GROUP BY customer_id, full_name
ORDER BY total_appointments DESC, completed_appointments DESC;
