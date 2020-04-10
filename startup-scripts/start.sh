#!/bin/bash
docker-compose down
docker-compose build
docker-compose up -d
docker exec -it development_eagle python3 manager.py $@
