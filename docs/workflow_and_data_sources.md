# Glam Hub – Workflow and Data Sources

## Project Context

Glam Hub is a salon and parlour management software designed to support the full operational flow from appointment booking to post-service customer engagement. The system connects appointment handling, salon floor execution, billing, CRM activity, and inventory-related updates into one connected workflow.

The main business flow studied in the first week was:

**Appointment → Check-in → Service Execution → Billing & Payment → Feedback / Loyalty → Inventory Trigger**

## Workflow Understanding

### 1. Appointment and Booking

A customer can initiate a booking through app, web, walk-in, or phone. During booking, the customer selects the branch, date and time, service, and stylist. Once the request is created, the system checks availability based on staff skills, room or station availability, service duration, and idle buffer. If a slot is available, the appointment is confirmed and the customer is notified. If not, the system suggests alternatives.

### 2. Arrival and Check-in

When the customer arrives, check-in can happen through a receptionist, POS terminal, or kiosk/mobile flow. At this point, the appointment status changes to checked-in and enters the queue. A stylist, room, or station is then assigned, and the salon floor management view is updated.

### 3. Service Execution

The stylist starts the service through the staff mobile app. The appointment status becomes in progress. During or after the service, the stylist records any product usage. This product usage connects the service workflow with inventory updates.

### 4. Billing and Payment

After service completion, the receptionist generates the invoice. The invoice may include services, products used, taxes, discounts, coupons, and package or membership redemptions. Payment is then accepted through one or more modes such as cash, card, wallet, or UPI. Once paid, the invoice status changes to paid and a receipt is issued.

### 5. Post-Service Links

After payment, the system calculates staff commissions, records accounting-related audit entries, and sends customer feedback requests. The customer’s loyalty points are also updated as part of the CRM process.

### 6. Inventory Trigger

If recorded product usage reduces stock below a reorder threshold, the system generates a low-stock signal that can be used for procurement planning in later phases.

## Main Source Systems Identified

The initial source systems identified for this project are listed below.

### Web / App Booking Source
This source captures online appointment requests, customer booking details, selected branch, selected services, selected stylist, and preferred slot timing.

### POS System
This source supports front desk and billing operations. It handles check-in, service confirmation, invoice creation, payment capture, and receipt generation.

### Staff Mobile App
This source supports service execution actions such as starting a service, completing a service, and recording product usage.

### Inventory System
This source maintains product stock information, quantity changes, reorder thresholds, and inventory-linked product movement details.

### CRM / Loyalty Process
This source or subsystem handles post-service engagement such as feedback requests, notification activity, and loyalty point updates.

## Key Data Entities Observed

Based on the workflow, the main entities identified during the first week are:

- Branch
- Customer
- Appointment
- Service
- Staff / Stylist
- Invoice
- Payment
- Product
- Inventory Movement
- Commission
- Loyalty / Feedback
- Notification

These entities will not all be modeled in full detail immediately, but they shape the direction of the database and pipeline design.

## High-Level Data Movement

At a high level, data moves through the system in the following way:

1. **Booking channels** create appointment-related operational data.
2. **Salon execution systems** update appointment status and service progress.
3. **Billing systems** generate invoices and payment records.
4. **Inventory-related actions** are triggered by product consumption during services.
5. **CRM-related actions** are triggered after successful service completion and payment.
6. **Downstream analytics and reporting** can later use appointment, billing, service, and inventory data for dashboards and operational reporting.

## Integration Points

The most important integration points identified during Week 1 are:

- Booking flow to appointment records
- Check-in flow to queue and service assignment
- Service execution to product usage
- Product usage to inventory reduction
- Appointment completion to invoice generation
- Invoice payment to commission and accounting updates
- Service completion and payment to feedback and loyalty updates

## Engineering and Analyst Coordination Points

The following areas were identified as important for coordination with software engineers and analysts:

- Appointment status flow and lifecycle definitions
- Service completion and billing dependency
- Product usage capture during service
- Reporting expectations for appointments, revenue, staff utilization, and inventory activity
- Data ownership across booking, POS, inventory, and CRM functions

## Initial Assumptions

- A customer may book multiple appointments over time.
- One appointment may involve one or more services, though an initial simplified schema may use one primary service and allow later extension.
- Billing happens after service completion.
- Product usage can affect inventory counts directly.
- CRM and loyalty actions occur after completion of billing/payment.

## Week 1 Output Summary

The work completed in this phase focused on understanding how the salon business process translates into data movement across operational systems. This understanding forms the base for the next phase, where schema design, database selection, and storage strategy are defined.

