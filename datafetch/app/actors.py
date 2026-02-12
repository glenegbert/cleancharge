import dramatiq
from dramatiq.brokers.redis import RedisBroker

broker = RedisBroker(url="redis://redis:6379")
dramatiq.set_broker(broker)

# This is currently being queued via a local cron which you can add like this in macos:

# printf '*/5 * * * * cd /Users/glenegbert/Projects/cleancharge && /usr/local/bin/docker-compose exec -T datafetchTH=/usr/local/bin:/usr/bin:/bin\n*/5 * * * * cd /Users/glenegbert/Projects/cleancharge && docker-compose exec -T datafetch python -c "from actors import run_forecast; run_forecast.send()"\n' > /tmp/my_crontab
# crontab /tmp/my_crontab

@dramatiq.actor
def run_forecast():
    from jobs.forecast import main
    main()
