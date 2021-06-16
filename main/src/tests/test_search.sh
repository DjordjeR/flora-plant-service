#!/bin/bash

# Tests the search function

cd ..
sed -i 's/AUTH_ON=true/AUTH_ON=false/g' ../docker/.env.docker

docker-compose up --build -d
pytest tests/tests_py/test_search.py
docker-compose down -v