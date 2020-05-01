#!/bin/bash
docker-compose down
docker-compose build
docker-compose up -d
cat $HOME/.bash_profile | grep -q "eagleeye"
if [ $? != 0 ]; then
  echo "alias eagleeye='`pwd`/eagleeye'" >> ~/.bash_profile
fi
source  ~/.bash_profile
