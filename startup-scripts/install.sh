#!/bin/bash
docker-compose down
docker-compose build
docker-compose up -d
cat $HOME/.bash_profile | grep -q "$(pyenv init -)"
if [ $? != 0 ]; then
  echo "alias eagleeye='`pwd`/eagleeye'" >> ~/.bash_profile
  source ~/.bash_profile
fi
