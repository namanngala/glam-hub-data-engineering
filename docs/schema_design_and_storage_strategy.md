# Glam Hub – Schema Design and Storage Strategy

## Project Context

This document summarizes the main database and storage design decisions made for the Glam Hub – Salon & Parlour Management Software project during the second week. The goal of this phase was to define a practical database structure for the core workflow while keeping the design at a manageable junior-to-mid-level scope.

## Database Choice

For this project, **PostgreSQL** was selected as the preferred database.

### Why PostgreSQL was chosen

- It supports structured relational design well for operational systems.
- It is strong for transactional workloads such as appointments, billing, and staff assignment.
- It provides solid SQL capabilities for future reporting and analytical extensions.
- It is a practical choice for both development and staging environments.

MySQL was also considered, but PostgreSQL was preferred because it gives better flexibility for future reporting views, indexing strategies, and expansion into richer analytical workloads.

## Core Schema Design

The schema was designed around the key entities requested in the task sheet:

- Customers
- Appointments
- Invoices
- Products
- Staff

To make the model more practical and relationally complete, a few supporting tables were also added:

- Branches
- Services
- Invoice Items

This keeps the schema realistic without making it unnecessarily large.

## Main Tables Included

### 1. branches
Stores salon branch details such as location, contact information, and branch status.

### 2. customers
Stores customer profile details such as name, contact information, and loyalty-related fields.

### 3. staff
Stores employee and stylist details, including branch assignment, role, specialization, and active status.

### 4. services
Stores the service catalog offered by the salon, including category, duration, price, and active flag.

### 5. products
Stores product details that may be consumed during a service or billed to a customer. This includes pricing and branch-level stock-related fields.

### 6. appointments
Stores booking and service lifecycle data. This includes customer assignment, branch, staff assignment, service selection, booking channel, appointment time, and service status.

### 7. invoices
Stores invoice header information generated after service completion. This includes subtotal, tax, discount, total amount, and invoice status.

### 8. invoice_items
Stores line-level billing entries. Each line can represent either a service or a product depending on the item type.

## Relationship Thinking

The main relationship design used in this phase was:

- One branch can have many staff records.
- One branch can have many products.
- One branch can have many appointments.
- One customer can have many appointments.
- One staff member can be assigned to many appointments.
- One service can be linked to many appointments.
- One appointment is expected to generate one invoice.
- One invoice can contain many invoice items.
- Invoice items can refer to a service or a product.

This gives the schema enough structure to support booking, service execution, and billing without expanding too early into every downstream process.

## Why the Schema Was Kept Moderate

The workflow includes inventory, CRM, loyalty, commission, and accounting-related processes. However, all of those were not fully expanded into separate tables in this phase. The reason is that this week’s focus was the **initial operational database structure** for the main business flow.

A moderate schema helps keep the design understandable while leaving room for later expansion into:

- inventory movement tracking
- payments
- commissions
- loyalty transactions
- notifications
- procurement

## Environment Setup Approach

The initial setup approach considered for the project is:

- **Development Environment:** local PostgreSQL setup for schema design and query testing
- **Staging Environment:** controlled environment to validate schema behavior and future ETL/data flow testing
- **Production Consideration:** to be defined in later phases after pipeline and validation work is completed

At this stage, the environment work is still conceptual and planning-focused, not a full production deployment.

## Data Storage Strategy

### Transactional Storage
Operational data such as customers, appointments, staff, invoices, and products should be stored in normalized relational tables inside the central PostgreSQL database.

### Reporting / Analytical Consideration
Although analytics is not the main focus of Week 2, the schema is designed so that later phases can build reporting-ready tables or views on top of the operational database.

### Document / Artifact Storage
If the system later supports image uploads, digital bills, or CRM attachments, such files should be stored outside the database in object storage, while metadata references should remain in database tables.

### Backup and Recovery Thinking
A simple backup and recovery approach should include:
- periodic database backups
- schema version tracking
- restore validation in staging before production-level usage

## Performance and Optimization Notes

At this stage, performance work is only at a basic planning level. The main considerations identified are:

- use primary keys and foreign keys consistently
- index frequently joined or filtered columns such as appointment_id, customer_id, staff_id, branch_id, and invoice_id
- keep invoice line-item design separate from invoice headers
- avoid excessive denormalization too early

More advanced tuning can happen in later phases once queries and pipelines become more concrete.

## Assumptions

- A customer can visit multiple branches across time, even if one preferred branch is stored.
- Each appointment is linked to one main service in the initial version.
- Billing happens after the service is completed.
- Invoices may contain service and product line items together.
- The current schema is the foundational operational model and can be extended later.

project. This creates a clear base for future pipeline development, integration work, and reporting support.

