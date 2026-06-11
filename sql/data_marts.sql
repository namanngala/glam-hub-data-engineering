-- Week 7 data marts

CREATE OR REPLACE VIEW mart_revenue AS
SELECT
    b.branch_name,
    s.service_name,
    COUNT(DISTINCT i.invoice_id) AS invoice_count,
    SUM(i.total_amount) AS total_revenue,
    AVG(i.total_amount) AS avg_invoice_value
FROM invoices i
LEFT JOIN appointments a
    ON i.appointment_id = a.appointment_id
LEFT JOIN branches b
    ON a.branch_id = b.branch_id
LEFT JOIN services s
    ON a.primary_service_id = s.service_id
GROUP BY b.branch_name, s.service_name
ORDER BY total_revenue DESC;

CREATE OR REPLACE VIEW mart_customer_insights AS
SELECT
    c.customer_id,
    c.full_name,
    c.loyalty_points,
    COUNT(DISTINCT a.appointment_id) AS total_bookings,
    SUM(CASE WHEN a.status = 'Completed' THEN 1 ELSE 0 END) AS completed_bookings,
    SUM(i.total_amount) AS total_spend
FROM customers c
LEFT JOIN appointments a
    ON c.customer_id = a.customer_id
LEFT JOIN invoices i
    ON a.appointment_id = i.appointment_id
GROUP BY c.customer_id, c.full_name, c.loyalty_points
ORDER BY total_spend DESC NULLS LAST;
