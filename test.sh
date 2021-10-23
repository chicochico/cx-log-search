#!/usr/bin/env bash
set -e

docker-compose build
docker-compose up -d db

sleep 2

docker-compose run --entrypoint python log_service -m logger.populate_db
docker-compose run --entrypoint pytest log_service
