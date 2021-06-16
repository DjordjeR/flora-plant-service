#!/bin/bash

# Tests every request in a scenario where every servise should be working with AUTH_ON=true in .env (NOT INCLUDING THE SEARCH SERVICE)

cd ..
sed -i 's/AUTH_ON=false/AUTH_ON=true/g' ../docker/.env.docker

docker-compose up --build -d
sleep 10s # to let some time for the container initialisation
pytest tests/tests_py/test_AUTH_ON.py
docker-compose down -v