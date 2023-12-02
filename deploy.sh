#!/bin/bash -ex

git pull
docker compose build
docker compose run --rm --user root bigfive pdm run ./manage.py collectstatic --noinput --clear
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
docker image prune -f
