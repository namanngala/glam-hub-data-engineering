-- Integrated booking, service, and billing views

CREATE OR REPLACE VIEW vw_booking_service_billing AS
SELECT
    a.appointment_id,
    a.customer_id,
    c.full_name AS customer_name,
    a.branch_id,
    b.branch_name,
    a.staff_id,
    s.full_name AS staff_name,
    a.primary_service_id,
    sv.service_name,
    sv.category,
    a.appointment_datetime,
    a.status,
    a.booking_channel,
    i.invoice_id,
    i.invoice_date,
    i.subtotal,
    i.tax_amount,
    i.discount_amount,
    i.total_amount,
    i.invoice_status
FROM appointments a
LEFT JOIN customers c
    ON a.customer_id = c.customer_id
LEFT JOIN branches b
    ON a.branch_id = b.branch_id
LEFT JOIN staff s
    ON a.staff_id = s.staff_id
LEFT JOIN services sv
    ON a.primary_service_id = sv.service_id
LEFT JOIN invoices i
    ON a.appointment_id = i.appointment_id;

CREATE OR REPLACE VIEW vw_invoice_service_detail AS
SELECT
    i.invoice_id,
    i.invoice_date,
    a.appointment_id,
    b.branch_name,
    c.full_name AS customer_name,
    sv.service_name,
    sv.category,
    i.total_amount
FROM invoices i
LEFT JOIN appointments a
    ON i.appointment_id = a.appointment_id
LEFT JOIN branches b
    ON a.branch_id = b.branch_id
LEFT JOIN customers c
    ON i.customer_id = c.customer_id
LEFT JOIN services sv
    ON a.primary_service_id = sv.service_id;
