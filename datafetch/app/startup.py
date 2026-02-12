import clickhouse_connect

from clients.watttime import WattTimeClient

client = WattTimeClient()
ch = clickhouse_connect.get_client(host="clickhouse", username="default", password="default")
print("WattTimeClient ready: client")
print("ClickHouse ready: ch")
