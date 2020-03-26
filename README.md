# EagleEye
Northrop Grumman Group Research Project

Description:

Coming Soon.

Instructions for developers:

Docker Command Shortcuts:

If you want to see logs:

    Start:
        1. docker-compose build (Applies changes to containers/creates)
        2. docker-compose up
    Stop:
        1. ctrl-c
        2. docker-compose down

If you do not want to see logs:

    Start:
        1. docker-compose build (Applies changes to containers/creates)
        1. docker-compose up -d
    Stop:
        2. docker-compose down

Debugging documentation:
    
    I ran into the issue where changing the database version in the .yml file will corrupt the current image/volumes of the database locally

    I fixed the issue by wiping out the current images/volumes and rebuilding them from scratch using the following commands:

    1. Running either command to delete old volumes:

        docker-compose rm -v
        docker system prune --force --volumes

    2. Deleting ALL the contents of the "development-db-data" folder afterwards:

        rm -rf ./development-db-data/* (make sure hidden files are gone as well)

    3. Rebuilding the containers:

        docker-compose build




