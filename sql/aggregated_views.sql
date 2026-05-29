-- Aggregated datasets / reporting views

CREATE OR REPLACE VIEW vw_branch_revenue_summary AS
SELECT
    branch_id,
    branch_name,
    COUNT(DISTINCT invoice_id) AS invoice_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_invoice_value
FROM vw_booking_service_billing
GROUP BY branch_id, branch_name
ORDER BY total_revenue DESC;

CREATE OR REPLACE VIEW vw_service_revenue_summary AS
SELECT
    service_name,
    category,
    COUNT(DISTINCT appointment_id) AS appointment_count,
    SUM(total_amount) AS total_revenue
FROM vw_booking_service_billing
GROUP BY service_name, category
ORDER BY total_revenue DESC;
