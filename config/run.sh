#!/usr/bin/env bash



echo 'Waiting for RabbitMQ...'

while ! nc -z ${RABBITMQ_HOST} 5672; do

  sleep 0.1

done
echo 'RabbitMQ Initialization completed'

echo 'Waiting for Fuseki Server...'

while ! nc -z ${FUSEKI_SERVER_HOST} 3030; do

  sleep 0.1

done
echo 'Fuseki Server Initialization completed'

python init_fuseki_server.py
echo 'Saro Dataset loaded with initial data'


python consume.py
