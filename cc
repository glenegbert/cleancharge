#!/usr/bin/env bash
set -e

# need to symlink cc to something in PATH
# like ln -s ~/Projects/cleancharge/cc /usr/local/bin/cc

cd "$(dirname "$(readlink -f "$0")")"

case "$1" in
  up)    docker-compose up -d ;;
  down)  docker-compose down ;;
  build) docker-compose build ;;
  fetch) docker-compose exec datafetch python forecast_job.py ;;
  ch)
    case "$2" in
      sql) docker-compose exec clickhouse clickhouse-client --user default --password default ;;
      *)   echo "Usage: cc ch sql" ;;
    esac
    ;;
  *)     docker-compose exec "$@" ;;
esac
