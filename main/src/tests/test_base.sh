#!/bin/bash

# Tests every request in a scenario where every servise should be working

cd ..

docker-compose up --build -d
pytest tests/tests_py/test_base.py
docker-compose down -v