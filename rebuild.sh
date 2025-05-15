# !/bin/bash

docker-compose down -v
git fetch origin
git reset --hard origin/main
git clean -fd 
git pull
docker-compose up --build -d