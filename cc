#!/usr/bin/env bash
set -e

# need to symlink cc to something in PATH
# like ln -s ~/Projects/cleancharge/cc /usr/local/bin/cc

cd "$(dirname "$(readlink -f "$0")")"

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
      sql)  docker-compose exec clickhouse clickhouse-client --user default --password default ;;
      size) docker-compose exec clickhouse clickhouse-client --user default --password default --query "SELECT table, formatReadableSize(sum(bytes_on_disk)) AS size, sum(rows) AS rows FROM system.parts WHERE active GROUP BY table ORDER BY table" ;;
      *)    echo "Usage: cc ch {sql|size}" ;;
    esac
    ;;
  datafetch)
    case "$2" in
      python)  docker-compose exec datafetch python ;;
      logs)    docker-compose logs -f datafetch ;;
      fetch)   docker-compose exec datafetch python -m jobs.forecast ;;
      enqueue) docker-compose exec datafetch python -c "from actors import run_forecast; run_forecast.send()" ;;
      *)       echo "Usage: cc datafetch {python|logs|fetch|enqueue}" ;;
    esac
    ;;
  *) echo "Usage: cc {system|ch|datafetch}" ;;
esac
