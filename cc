#!/usr/bin/env bash
set -e

# need to symlink cc to something in PATH
# like ln -s ~/Projects/cleancharge/cc /usr/local/bin/cc

cd "$(dirname "$(readlink -f "$0")")"

case "$1" in
  up)    docker-compose up -d ;;
  down)  docker-compose down ;;
  build) docker-compose build ;;
  *)     docker-compose exec "$@" ;;
esac
