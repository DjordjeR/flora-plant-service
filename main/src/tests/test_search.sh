#!/bin/bash

# Tests the search function

cd ..

docker-compose up --build -d
pytest tests/tests_py/test_search.py
docker-compose down -v