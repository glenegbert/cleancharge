import dramatiq
from dramatiq.brokers.redis import RedisBroker

broker = RedisBroker(url="redis://redis:6379")
dramatiq.set_broker(broker)

# This is currently being queued via a local cron which you can add like this in macos:
# echo 'PATH=/usr/local/bin:/usr/bin:/bin' > /tmp/my_crontab
# echo '*/5 * * * * cd /Users/glenegbert/Projects/cleancharge && docker-compose exec -T datafetch python -c
# "from actors import run_forecast; run_forecast.send()"' >> /tmp/my_crontab
# crontab /tmp/my_crontab


@dramatiq.actor
def run_forecast():
    from lib.alerts import alert_from_exception
    try:
        from jobs.forecast import main
        main()
    except Exception as e:
        alert_from_exception("run_forecast", e)
        raise
