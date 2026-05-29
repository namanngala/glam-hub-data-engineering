-- Basic performance indexes for integration and aggregation queries

CREATE INDEX IF NOT EXISTS idx_appointments_customer_id
    ON appointments(customer_id);

CREATE INDEX IF NOT EXISTS idx_appointments_branch_id
    ON appointments(branch_id);

CREATE INDEX IF NOT EXISTS idx_appointments_staff_id
    ON appointments(staff_id);

CREATE INDEX IF NOT EXISTS idx_appointments_service_id
    ON appointments(primary_service_id);

CREATE INDEX IF NOT EXISTS idx_invoices_appointment_id
    ON invoices(appointment_id);

CREATE INDEX IF NOT EXISTS idx_invoices_customer_id
    ON invoices(customer_id);

CREATE INDEX IF NOT EXISTS idx_invoice_items_invoice_id
    ON invoice_items(invoice_id);
