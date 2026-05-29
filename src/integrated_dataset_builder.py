from pathlib import Path
import pandas as pd


RAW_DIR = Path("data/raw")
ANALYTICS_DIR = Path("data/analytics")


def main() -> None:
    ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)

    appointments = pd.read_csv(RAW_DIR / "appointments.csv")
    invoices = pd.read_csv(RAW_DIR / "invoices.csv")
    invoice_items = pd.read_csv(RAW_DIR / "invoice_items.csv")
    customers = pd.read_csv(RAW_DIR / "customers.csv")
    staff = pd.read_csv(RAW_DIR / "staff.csv")
    services = pd.read_csv(RAW_DIR / "services.csv")
    branches = pd.read_csv(RAW_DIR / "branches.csv")

    integrated = (
        appointments
        .merge(customers[["customer_id", "full_name"]], on="customer_id", how="left")
        .merge(staff[["staff_id", "full_name"]].rename(columns={"full_name": "staff_name"}), on="staff_id", how="left")
        .merge(branches[["branch_id", "branch_name"]], on="branch_id", how="left")
        .merge(services[["service_id", "service_name", "category", "base_price"]], left_on="primary_service_id", right_on="service_id", how="left")
        .merge(invoices[["invoice_id", "appointment_id", "invoice_date", "subtotal", "tax_amount", "discount_amount", "total_amount", "invoice_status"]], on="appointment_id", how="left")
    )

    integrated.to_csv(ANALYTICS_DIR / "integrated_booking_service_billing.csv", index=False)
    print("Created analytics/integrated_booking_service_billing.csv")


if __name__ == "__main__":
    main()
