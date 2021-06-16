#!/bin/bash

# Stops the keycloak container and tests authentication requests
# The container is started after the test

cd ..
sed -i 's/AUTH_ON=true/AUTH_ON=false/g' ../docker/.env.docker

docker-compose up --build -d 
sleep 10s # to let some time for the container initialisation
docker container stop flora-plant-service_keycloak_1 
sleep 2s
pytest tests/tests_py/test_no_auth.py
docker-compose down -v