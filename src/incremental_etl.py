from pathlib import Path
import json
import pandas as pd


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
ANALYTICS_DIR = Path("data/analytics")
STATE_FILE = Path("data/last_run.json")


def load_last_run() -> str:
    if not STATE_FILE.exists():
        return "1900-01-01 00:00:00"
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f).get("last_processed_timestamp", "1900-01-01 00:00:00")


def save_last_run(value: str) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"last_processed_timestamp": value}, f, indent=2)


def standardize_appointments(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["status"] = df["status"].fillna("Confirmed").str.strip().str.title()
    df["booking_channel"] = df["booking_channel"].fillna("App").str.strip().str.title()
    df["appointment_datetime"] = pd.to_datetime(df["appointment_datetime"], errors="coerce")
    df["checked_in_at"] = pd.to_datetime(df["checked_in_at"], errors="coerce")
    df["completed_at"] = pd.to_datetime(df["completed_at"], errors="coerce")
    return df


def standardize_invoices(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in ["subtotal", "tax_amount", "discount_amount", "total_amount"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
    df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")
    df["invoice_status"] = df["invoice_status"].fillna("Pending").str.strip().str.title()
    return df


def build_analytics(customers, branches, staff, services, appointments, invoices, invoice_items, products):
    analytics_appointments = (
        appointments
        .merge(customers[["customer_id", "full_name"]], on="customer_id", how="left")
        .merge(branches[["branch_id", "branch_name"]], on="branch_id", how="left")
        .merge(staff[["staff_id", "full_name"]].rename(columns={"full_name": "staff_name"}), on="staff_id", how="left")
        .merge(services[["service_id", "service_name", "category"]], left_on="primary_service_id", right_on="service_id", how="left")
        .drop(columns=["service_id"])
    )

    analytics_invoice_summary = (
        invoices
        .merge(appointments[["appointment_id", "branch_id", "staff_id", "primary_service_id"]], on="appointment_id", how="left")
        .merge(branches[["branch_id", "branch_name"]], on="branch_id", how="left")
        .merge(customers[["customer_id", "full_name"]], on="customer_id", how="left")
        .merge(services[["service_id", "service_name", "category"]], left_on="primary_service_id", right_on="service_id", how="left")
        .drop(columns=["service_id"])
    )

    item_enriched = (
        invoice_items
        .merge(invoices[["invoice_id", "invoice_date"]], on="invoice_id", how="left")
        .merge(services[["service_id", "service_name"]], on="service_id", how="left")
        .merge(products[["product_id", "product_name"]], on="product_id", how="left")
    )
    analytics_service_revenue = (
        item_enriched[item_enriched["item_type"].str.lower() == "service"]
        .groupby(["service_id", "service_name"], dropna=False, as_index=False)
        .agg(total_quantity=("quantity", "sum"), total_revenue=("line_total", "sum"))
    )

    return analytics_appointments, analytics_invoice_summary, analytics_service_revenue


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)

    last_run = pd.Timestamp(load_last_run())

    branches = pd.read_csv(RAW_DIR / "branches.csv")
    customers = pd.read_csv(RAW_DIR / "customers.csv")
    staff = pd.read_csv(RAW_DIR / "staff.csv")
    services = pd.read_csv(RAW_DIR / "services.csv")
    products = pd.read_csv(RAW_DIR / "products.csv")
    appointments = pd.read_csv(RAW_DIR / "appointments.csv")
    invoices = pd.read_csv(RAW_DIR / "invoices.csv")
    invoice_items = pd.read_csv(RAW_DIR / "invoice_items.csv")

    appointments = standardize_appointments(appointments)
    invoices = standardize_invoices(invoices)

    incremental_appointments = appointments[appointments["appointment_datetime"] > last_run].copy()
    incremental_invoices = invoices[invoices["invoice_date"] > last_run.normalize()].copy()

    incremental_appointments.to_csv(PROCESSED_DIR / "appointments_clean.csv", index=False)
    incremental_invoices.to_csv(PROCESSED_DIR / "invoices_clean.csv", index=False)

    analytics_appointments, analytics_invoice_summary, analytics_service_revenue = build_analytics(
        customers, branches, staff, services, appointments, invoices, invoice_items, products
    )

    analytics_appointments.to_csv(ANALYTICS_DIR / "analytics_appointments.csv", index=False)
    analytics_invoice_summary.to_csv(ANALYTICS_DIR / "analytics_invoice_summary.csv", index=False)
    analytics_service_revenue.to_csv(ANALYTICS_DIR / "analytics_service_revenue.csv", index=False)

    max_appt_time = appointments["appointment_datetime"].max()
    save_last_run(str(max_appt_time))


if __name__ == "__main__":
    main()
