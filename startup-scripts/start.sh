#!/bin/bash



# echo "All Arguments values:" $@
docker-compose build
docker-compose up
# docker exec -it development-eagle python3 manager.py $@
