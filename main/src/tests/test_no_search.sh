#!/bin/bash

# Test when the search service is not available

cd ..
sed -i 's/AUTH_ON=true/AUTH_ON=false/g' ../docker/.env.docker

docker-compose up --build -d  
sleep 10s # to let some time for the container initialisation
docker container stop flora-plant-service_meilisearch_1 
docker container stop flora-plant-service_scraping_service_1
sleep 2s
pytest tests/tests_py/test_no_search.py
docker-compose down -v