from pathlib import Path
import pandas as pd


ANALYTICS_DIR = Path("data/analytics")


def main() -> None:
    integrated = pd.read_csv(ANALYTICS_DIR / "integrated_booking_service_billing.csv")

    agg_branch_revenue = (
        integrated.groupby(["branch_id", "branch_name"], dropna=False, as_index=False)
        .agg(
            invoice_count=("invoice_id", "nunique"),
            total_revenue=("total_amount", "sum"),
            avg_invoice_value=("total_amount", "mean")
        )
        .sort_values("total_revenue", ascending=False)
    )

    agg_service_revenue = (
        integrated.groupby(["service_name", "category"], dropna=False, as_index=False)
        .agg(
            appointment_count=("appointment_id", "nunique"),
            total_revenue=("total_amount", "sum")
        )
        .sort_values("total_revenue", ascending=False)
    )

    agg_branch_revenue.to_csv(ANALYTICS_DIR / "agg_branch_revenue.csv", index=False)
    agg_service_revenue.to_csv(ANALYTICS_DIR / "agg_service_revenue.csv", index=False)

    print("Created analytics/agg_branch_revenue.csv")
    print("Created analytics/agg_service_revenue.csv")


if __name__ == "__main__":
    main()
