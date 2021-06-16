#!/bin/bash

# Tests every request in a scenario where every servise should be working (NOT INCLUDING THE SEARCH SERVICE)

cd ..
sed -i 's/AUTH_ON=true/AUTH_ON=false/g' ../docker/.env.docker

docker-compose up --build -d
sleep 10s # to let some time for the container initialisation
pytest tests/tests_py/test_base.py
docker-compose down -v