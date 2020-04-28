#!/bin/bash
docker-compose down
docker-compose build
docker-compose up -d
echo "alias eagleeye='`pwd`/eagleeye'" >> ~/.bash_profile
source ~/.bash_profile
