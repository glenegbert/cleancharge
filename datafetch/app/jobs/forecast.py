import logging
from datetime import datetime

import clickhouse_connect

from clients.watttime import WattTimeClient

logging.basicConfig(level=logging.INFO)


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
    ch = clickhouse_connect.get_client(host="clickhouse", username="default", password="default")
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
    rows = parse_forecast(data)
    count = insert_rows(rows)
    print(f"Inserted {count} rows into watttime_forecasts.")


if __name__ == "__main__":
    main()
