from pathlib import Path
import pandas as pd


RAW_DIR = Path("data/raw")


def check_duplicates(df: pd.DataFrame, key: str) -> int:
    return int(df.duplicated(subset=[key]).sum())


def check_missing(df: pd.DataFrame, columns: list[str]) -> dict:
    return {col: int(df[col].isna().sum()) for col in columns}


def main() -> None:
    customers = pd.read_csv(RAW_DIR / "customers.csv")
    staff = pd.read_csv(RAW_DIR / "staff.csv")
    services = pd.read_csv(RAW_DIR / "services.csv")
    products = pd.read_csv(RAW_DIR / "products.csv")
    appointments = pd.read_csv(RAW_DIR / "appointments.csv")
    invoices = pd.read_csv(RAW_DIR / "invoices.csv")
    invoice_items = pd.read_csv(RAW_DIR / "invoice_items.csv")

    print("Duplicate checks")
    print("customers:", check_duplicates(customers, "customer_id"))
    print("staff:", check_duplicates(staff, "staff_id"))
    print("services:", check_duplicates(services, "service_id"))
    print("products:", check_duplicates(products, "product_id"))
    print("appointments:", check_duplicates(appointments, "appointment_id"))
    print("invoices:", check_duplicates(invoices, "invoice_id"))
    print("invoice_items:", check_duplicates(invoice_items, "invoice_item_id"))

    print("\nMissing value checks")
    print("appointments:", check_missing(appointments, ["customer_id", "branch_id", "staff_id", "primary_service_id", "status"]))
    print("invoices:", check_missing(invoices, ["appointment_id", "customer_id", "total_amount", "invoice_status"]))

    print("\nSimple rule checks")
    print("negative total_amount rows:", int((invoices["total_amount"] < 0).sum()))
    print("invalid appointment statuses:", int((~appointments["status"].isin(['Confirmed', 'Checked-In', 'In Progress', 'Completed', 'Cancelled'])).sum()))


if __name__ == "__main__":
    main()
