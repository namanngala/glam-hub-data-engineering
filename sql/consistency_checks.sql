-- Data consistency checks

-- 1. Appointments with invalid status values
SELECT *
FROM appointments
WHERE status NOT IN ('Confirmed', 'Checked-In', 'In Progress', 'Completed', 'Cancelled');

-- 2. Appointments missing key references
SELECT *
FROM appointments
WHERE customer_id IS NULL
   OR branch_id IS NULL
   OR staff_id IS NULL
   OR primary_service_id IS NULL;

-- 3. Completed appointments without completion timestamp
SELECT *
FROM appointments
WHERE status = 'Completed'
  AND completed_at IS NULL;

-- 4. Invoices linked to appointments that are not completed
SELECT i.*
FROM invoices i
LEFT JOIN appointments a
    ON i.appointment_id = a.appointment_id
WHERE a.status <> 'Completed';

-- 5. Duplicate appointment ids
SELECT appointment_id, COUNT(*) AS duplicate_count
FROM appointments
GROUP BY appointment_id
HAVING COUNT(*) > 1;
