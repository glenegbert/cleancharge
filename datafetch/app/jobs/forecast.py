import logging
from datetime import datetime

from lib.alerts import insert_alert
from lib.ch import get_client
from clients.watttime.v3 import WattTimeClient

logging.basicConfig(level=logging.INFO)

EXPECTED_META_KEYS = {"region", "signal_type", "units", "generated_at"}
EXPECTED_POINT_KEYS = {"point_time", "value"}


def validate_response(data):
    if "meta" not in data or "data" not in data:
        insert_alert("schema_change", "forecast_job", f"Missing top-level keys. Got: {set(data.keys())}")
        raise ValueError(f"Invalid response: missing top-level keys. Got: {set(data.keys())}")

    meta_keys = set(data["meta"].keys())
    if not EXPECTED_META_KEYS.issubset(meta_keys):
        insert_alert("schema_change", "forecast_job", f"Meta keys changed. Expected {EXPECTED_META_KEYS}, got {meta_keys}")

    if data["data"]:
        point_keys = set(data["data"][0].keys())
        if not EXPECTED_POINT_KEYS.issubset(point_keys):
            insert_alert("schema_change", "forecast_job", f"Point keys changed. Expected {EXPECTED_POINT_KEYS}, got {point_keys}")


def parse_forecast(data):
    """Flatten a WattTime forecast response into rows."""
    meta = data["meta"]
    region = meta["region"]
    signal_type = meta["signal_type"]
    units = meta["units"]
    generated_at = datetime.fromisoformat(meta["generated_at"])

    rows = []
    for point in data["data"]:
        rows.append((
            region,
            signal_type,
            units,
            generated_at,
            datetime.fromisoformat(point["point_time"]),
            point["value"],
        ))
    return rows


def insert_rows(rows):
    """Insert forecast rows into ClickHouse."""
    ch = get_client()
    ch.insert(
        "watttime_forecasts",
        rows,
        column_names=["region", "signal_type", "units", "generated_at", "point_time", "value"],
    )
    return len(rows)


def main():
    client = WattTimeClient()
    client.login()
    print("Fetching forecast...")
    data = client.get_forecast()
    validate_response(data)
    rows = parse_forecast(data)
    count = insert_rows(rows)
    print(f"Inserted {count} rows into watttime_forecasts.")


if __name__ == "__main__":
    main()
