from pathlib import Path
import pandas as pd


RAW_DIR = Path("data/raw")


def check_status_values(appointments: pd.DataFrame) -> pd.DataFrame:
    allowed = {"Confirmed", "Checked-In", "In Progress", "Completed", "Cancelled"}
    invalid = appointments[~appointments["status"].isin(allowed)].copy()
    invalid["issue"] = "Invalid appointment status"
    return invalid


def check_missing_keys(appointments: pd.DataFrame) -> pd.DataFrame:
    mask = (
        appointments["customer_id"].isna()
        | appointments["branch_id"].isna()
        | appointments["staff_id"].isna()
        | appointments["primary_service_id"].isna()
    )
    missing = appointments[mask].copy()
    missing["issue"] = "Missing required foreign key"
    return missing


def check_completed_without_timestamp(appointments: pd.DataFrame) -> pd.DataFrame:
    bad = appointments[
        (appointments["status"] == "Completed") &
        (appointments["completed_at"].isna() | (appointments["completed_at"].astype(str).str.strip() == ""))
    ].copy()
    bad["issue"] = "Completed appointment missing completed_at"
    return bad


def check_invoice_to_appointment(invoices: pd.DataFrame, appointments: pd.DataFrame) -> pd.DataFrame:
    merged = invoices.merge(
        appointments[["appointment_id", "status"]],
        on="appointment_id",
        how="left"
    )
    bad = merged[merged["status"] != "Completed"].copy()
    bad["issue"] = "Invoice linked to non-completed appointment"
    return bad


def main() -> None:
    appointments = pd.read_csv(RAW_DIR / "appointments.csv")
    invoices = pd.read_csv(RAW_DIR / "invoices.csv")

    issues = pd.concat([
        check_status_values(appointments),
        check_missing_keys(appointments),
        check_completed_without_timestamp(appointments),
        check_invoice_to_appointment(invoices, appointments)
    ], ignore_index=True)

    if issues.empty:
        print("All consistency checks passed.")
    else:
        print("Consistency issues found:")
        print(issues.head(20).to_string(index=False))


if __name__ == "__main__":
    main()
