#!/usr/bin/env bash
set -e

# need to symlink cc to something in PATH
# like ln -s ~/Projects/cleancharge/cc /usr/local/bin/cc

cd "$(dirname "$(readlink -f "$0")")"

source .env

case "$1" in
  system)
    case "$2" in
      up)    docker-compose up -d ;;
      down)  docker-compose down ;;
      build)   docker-compose build ;;
      restart) docker-compose down && docker-compose build && docker-compose up -d ;;
      *)     echo "Usage: cc system {up|down|build|restart}" ;;
    esac
    ;;
  ch)
    case "$2" in
      sql)  docker-compose exec clickhouse clickhouse-client --user "$CLICKHOUSE_USER" --password "$CLICKHOUSE_PASSWORD" ;;
      logs) docker-compose logs -f clickhouse ;;
      size) docker-compose exec clickhouse clickhouse-client --user "$CLICKHOUSE_USER" --password "$CLICKHOUSE_PASSWORD" --query "SELECT table, formatReadableSize(sum(bytes_on_disk)) AS size, sum(rows) AS rows FROM system.parts WHERE active GROUP BY table ORDER BY table" ;;
      migrate) docker-compose exec -T clickhouse clickhouse-client --user "$CLICKHOUSE_USER" --password "$CLICKHOUSE_PASSWORD" --multiquery < clickhouse/init/create_tables.sql ;;
      alerts) docker-compose exec clickhouse clickhouse-client --user "$CLICKHOUSE_USER" --password "$CLICKHOUSE_PASSWORD" --query "SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 20" ;;
      clear_logs) docker-compose down && docker volume rm cleancharge_clickhouse_data && docker-compose up -d ;;
      *)    echo "Usage: cc ch {sql|logs|size|migrate|alerts|clear_logs}" ;;
    esac
    ;;
  datafetch)
    case "$2" in
      python)  docker-compose exec datafetch python ;;
      logs)    docker-compose logs -f datafetch ;;
      fetch)   docker-compose exec datafetch python -m jobs.forecast ;;
      enqueue) docker-compose exec datafetch python -c "from actors import run_forecast; run_forecast.send()" ;;
      test)    docker-compose exec datafetch python -m pytest tests/ -v ;;
      *)       echo "Usage: cc datafetch {python|logs|fetch|enqueue|test}" ;;
    esac
    ;;
  *) echo "Usage: cc {system|ch|datafetch}" ;;
esac
