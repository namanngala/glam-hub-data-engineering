from pathlib import Path
import pandas as pd


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


def load_inputs():
    appointments = pd.read_csv(RAW_DIR / "appointments.csv")
    invoices = pd.read_csv(RAW_DIR / "invoices.csv")
    return appointments, invoices


def standardize_status(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["status"] = df["status"].fillna("Confirmed").str.strip().str.title()
    df["booking_channel"] = df["booking_channel"].fillna("App").str.strip().str.title()
    df["appointment_datetime"] = pd.to_datetime(df["appointment_datetime"], errors="coerce")
    df["checked_in_at"] = pd.to_datetime(df["checked_in_at"], errors="coerce")
    df["completed_at"] = pd.to_datetime(df["completed_at"], errors="coerce")
    return df


def derive_service_stage(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    stage_map = {
        "Confirmed": "Booked",
        "Checked-In": "Waiting",
        "In Progress": "Service Running",
        "Completed": "Service Finished",
        "Cancelled": "Closed"
    }
    df["service_stage"] = df["status"].map(stage_map).fillna("Unknown")
    return df


def simulate_recent_updates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    recent = df["status"].isin(["Checked-In", "In Progress", "Completed"])
    df["is_recent_update"] = recent
    return df


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    appointments, invoices = load_inputs()
    appointments = standardize_status(appointments)
    appointments = derive_service_stage(appointments)
    appointments = simulate_recent_updates(appointments)

    invoices["invoice_status"] = invoices["invoice_status"].fillna("Pending").str.strip().str.title()
    invoices["invoice_date"] = pd.to_datetime(invoices["invoice_date"], errors="coerce")

    appointments.to_csv(PROCESSED_DIR / "appointments_status_updates.csv", index=False)
    invoices.to_csv(PROCESSED_DIR / "invoices_status_ready.csv", index=False)

    print("Real-time style update files created in data/processed")


if __name__ == "__main__":
    main()
