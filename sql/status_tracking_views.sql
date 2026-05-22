-- Views for appointment and service status tracking

CREATE OR REPLACE VIEW vw_appointment_status_counts AS
SELECT
    branch_id,
    status,
    COUNT(*) AS appointment_count
FROM appointments
GROUP BY branch_id, status
ORDER BY branch_id, appointment_count DESC;

CREATE OR REPLACE VIEW vw_service_progress_summary AS
SELECT
    status,
    COUNT(*) AS total_records
FROM appointments
GROUP BY status
ORDER BY total_records DESC;

CREATE OR REPLACE VIEW vw_completed_services_by_staff AS
SELECT
    staff_id,
    COUNT(*) AS completed_services
FROM appointments
WHERE status = 'Completed'
GROUP BY staff_id
ORDER BY completed_services DESC;

CREATE OR REPLACE VIEW vw_daily_appointment_updates AS
SELECT
    DATE(appointment_datetime) AS appointment_date,
    status,
    COUNT(*) AS status_count
FROM appointments
GROUP BY DATE(appointment_datetime), status
ORDER BY appointment_date, status_count DESC;
