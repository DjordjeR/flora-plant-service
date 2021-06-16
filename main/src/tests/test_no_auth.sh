#!/bin/bash

# Stops the keycloak container and tests authentication requests
# The container is started after the test

cd ..

docker-compose up --build -d 
docker container stop docker_keycloak_1 
pytest tests/tests_py/test_no_auth.py
docker container stop docker_keycloak_1
docker-compose down -v