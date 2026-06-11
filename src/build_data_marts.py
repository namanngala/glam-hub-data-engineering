from pathlib import Path
import pandas as pd


RAW_DIR = Path("data/raw")
MART_DIR = Path("data/marts")


def main() -> None:
    MART_DIR.mkdir(parents=True, exist_ok=True)

    appointments = pd.read_csv(RAW_DIR / "appointments.csv")
    invoices = pd.read_csv(RAW_DIR / "invoices.csv")
    customers = pd.read_csv(RAW_DIR / "customers.csv")
    services = pd.read_csv(RAW_DIR / "services.csv")
    branches = pd.read_csv(RAW_DIR / "branches.csv")

    integrated = (
        appointments
        .merge(customers[["customer_id", "full_name", "loyalty_points"]], on="customer_id", how="left")
        .merge(branches[["branch_id", "branch_name"]], on="branch_id", how="left")
        .merge(services[["service_id", "service_name", "category"]], left_on="primary_service_id", right_on="service_id", how="left")
        .merge(invoices[["appointment_id", "invoice_id", "total_amount"]], on="appointment_id", how="left")
    )

    revenue_mart = (
        integrated.groupby(["branch_name", "service_name"], dropna=False, as_index=False)
        .agg(
            invoice_count=("invoice_id", "nunique"),
            total_revenue=("total_amount", "sum"),
            avg_invoice_value=("total_amount", "mean")
        )
        .sort_values("total_revenue", ascending=False)
    )

    customer_insights_mart = (
        integrated.groupby(["customer_id", "full_name", "loyalty_points"], dropna=False, as_index=False)
        .agg(
            total_bookings=("appointment_id", "nunique"),
            completed_bookings=("status", lambda x: (x == "Completed").sum()),
            total_spend=("total_amount", "sum")
        )
        .sort_values("total_spend", ascending=False)
    )

    revenue_mart.to_csv(MART_DIR / "mart_revenue.csv", index=False)
    customer_insights_mart.to_csv(MART_DIR / "mart_customer_insights.csv", index=False)

    print("Created revenue and customer insights marts")


if __name__ == "__main__":
    main()
