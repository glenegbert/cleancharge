import traceback
from datetime import datetime, timezone

from lib.ch import get_client


def insert_alert(alert_type, source, message, details=""):
    ch = get_client()
    ch.insert(
        "alerts",
        [(datetime.now(timezone.utc), alert_type, source, message, details)],
        column_names=["timestamp", "alert_type", "source", "message", "details"],
    )


def alert_from_exception(source, e):
    insert_alert(
        alert_type="unhandled_error",
        source=source,
        message=str(e),
        details=traceback.format_exc(),
    )
