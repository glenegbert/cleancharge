#!/bin/bash
set -e

# Install and start cron
crontab /etc/cron.d/forecast-cron
cron

# Run the main command (dramatiq worker)
exec "$@"
