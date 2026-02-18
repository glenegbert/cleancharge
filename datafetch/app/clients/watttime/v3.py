import logging
import os

import requests

log = logging.getLogger(__name__)

BASE_URL = "https://api.watttime.org"


class WattTimeClient:
    def __init__(self, username=None, password=None):
        username = username or os.environ.get("WATTTIME_USERNAME")
        password = password or os.environ.get("WATTTIME_PASSWORD")
        if not username or not password:
            raise ValueError(
                "Credentials required: pass username/password or set "
                "WATTTIME_USERNAME and WATTTIME_PASSWORD env vars."
            )
        self.username = username
        self.password = password
        self.token = None
        self.session = requests.Session()

    def login(self):
        """Authenticate with WattTime and cache the bearer token."""
        log.info("Logging in as %s", self.username)
        resp = self.session.get(
            f"{BASE_URL}/login", auth=(self.username, self.password)
        )
        resp.raise_for_status()
        token = resp.json().get("token")
        if not token:
            raise ValueError(f"No token in response: {resp.json()}")
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        log.info("Login successful")

    def get_forecast(self, region="CAISO_NORTH", signal_type="co2_moer", horizon_hours=72):
        """Fetch forecast data for a region and signal type."""
        if not self.token:
            self.login()

        log.info("Fetching forecast: region=%s signal_type=%s horizon_hours=%s", region, signal_type, horizon_hours)
        resp = self.session.get(
            f"{BASE_URL}/v3/forecast",
            params={
                "region": region,
                "signal_type": signal_type,
                "horizon_hours": horizon_hours,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        log.info("Received %d data points", len(data.get("data", [])))
        return data
