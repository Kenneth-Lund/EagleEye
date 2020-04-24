# EagleEye
Northrop Grumman Group Research Project

Description:
The goal of the project is to develop a tool to help government entities and private companies identify Personally Identifiable Information (PII) on their websites that exposes sensitive information. 

Utilize multiple technologies to build an application that is compatible with the Linux operating system  
Utilize predefined user data queries (phone number, email addresses, etc.) to extract relevant information

Instructions for developers:

    - ./startup-scripts/start.sh --url http://127.0.0.1:5000 --time 5 --keywords Username

    - url: initial url
    - time: max time to check a webpage for changes
    - keywords: a list of keywords you want to search for
    
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
Output documentation -- view output.py for 
    
   Different output options: 
    
   1. Statistics:
        -- outputs various meaningful mathematical calculations of the data including averages, counts, etc.
    
   2. All Phone Numbers
        -- outputs all phones numbers found and during what process
    
   3. All Social Security Numbers
         -- outputs all social security numbers found and during what process
    
   4  All Emails
         -- outputs all emails found and during what process
   
   5. All Keywords
         -- outputs all keywords found and during what process
    
   6. Machine-Readable:
        -- outputs a csv of the data



