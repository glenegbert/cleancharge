import dramatiq
from dramatiq.brokers.redis import RedisBroker

broker = RedisBroker(url="redis://redis:6379")
dramatiq.set_broker(broker)


@dramatiq.actor
def run_forecast():
    from jobs.forecast import main
    main()
