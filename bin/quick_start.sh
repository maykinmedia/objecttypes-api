#!/bin/sh

set -ex

wget https://raw.githubusercontent.com/maykinmedia/objecttypes-api/master/docker-compose-quickstart.yml -O docker-compose-qs.yml
docker-compose -f docker-compose-qs.yml up -d

sleep 10

docker-compose exec -T web src/manage.py loaddata demodata
