from pathlib import Path
import pandas as pd


RAW_DIR = Path("data/raw")
WAREHOUSE_DIR = Path("data/warehouse")


def main() -> None:
    WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)

    customers = pd.read_csv(RAW_DIR / "customers.csv")
    services = pd.read_csv(RAW_DIR / "services.csv")
    branches = pd.read_csv(RAW_DIR / "branches.csv")
    appointments = pd.read_csv(RAW_DIR / "appointments.csv")

    dim_customers = customers.copy()
    dim_customers.insert(0, "customer_key", range(1, len(dim_customers) + 1))

    dim_services = services.copy()
    dim_services.insert(0, "service_key", range(1, len(dim_services) + 1))

    dim_branch = branches.copy()
    dim_branch.insert(0, "branch_key", range(1, len(dim_branch) + 1))

    unique_dates = pd.to_datetime(appointments["appointment_datetime"], errors="coerce").dropna().dt.date.drop_duplicates()
    dim_date = pd.DataFrame({"full_date": sorted(unique_dates)})
    dim_date.insert(0, "date_key", range(1, len(dim_date) + 1))
    dim_date["month"] = pd.to_datetime(dim_date["full_date"]).dt.month
    dim_date["quarter"] = pd.to_datetime(dim_date["full_date"]).dt.quarter
    dim_date["year"] = pd.to_datetime(dim_date["full_date"]).dt.year

    dim_customers.to_csv(WAREHOUSE_DIR / "dim_customers.csv", index=False)
    dim_services.to_csv(WAREHOUSE_DIR / "dim_services.csv", index=False)
    dim_branch.to_csv(WAREHOUSE_DIR / "dim_branch.csv", index=False)
    dim_date.to_csv(WAREHOUSE_DIR / "dim_date.csv", index=False)

    print("Created warehouse dimension tables")


if __name__ == "__main__":
    main()
