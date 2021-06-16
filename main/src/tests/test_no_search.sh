#!/bin/bash

# Test when the search service is not available

cd ..

docker-compose up --build -d
pytest tests/tests_py/test_base.py
docker-compose down -v