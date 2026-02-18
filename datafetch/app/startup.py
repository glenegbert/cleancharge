from lib.ch import get_client
from clients.watttime.v3 import WattTimeClient

client = WattTimeClient()
ch = get_client()
print("WattTimeClient ready: client")
print("ClickHouse ready: ch")
