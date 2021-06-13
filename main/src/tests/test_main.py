import uvicorn
import pytest
import requests
import json

from app.main import get_application
from multiprocessing import Process

app = get_application()

base_url = "http://127.0.0.1:8000"


# Borrowed from https://stackoverflow.com/questions/57412825/how-to-start-a-uvicorn-fastapi-in-background-when-testing-with-pytest
def run_server():
    uvicorn.run(app, port=8080, loop="asyncio", lifespan="on")

@pytest.fixture
def server():
    proc = Process(target=run_server, args=(), daemon=True)
    proc.start() 
    yield
    proc.kill()


##################
##################


def test_plant_get():
    response = requests.get(base_url + "/plant")
    assert response.status_code == 200


# Create new plant
# def test_post_plant_new():
#     data = {'common_name': 'novinovinovi', 'latin_name': 'novinovinovi'}
#     response = requests.post(base_url + "/plant", json=data)

#     assert response.status_code == 200


# Try to create a duplicate
def test_post_plant_duplicate():
    data = {'common_name': 'gucci', 'latin_name': 'gucci'}
    response = requests.post(base_url + "/plant", json=data)

    assert response.status_code == 422


# Missing common_name parameter
def test_post_plant_missing_common_name():
    data = {'latin_name': 'gucci'}
    response = requests.post(base_url + "/plant", json=data)

    assert response.status_code == 422
   

# Missing latin_name parameter
def test_post_plant_missing_latin_name():
    data = {'common_name': 'gucci'}
    response = requests.post(base_url + "/plant", json=data)

    assert response.status_code == 422


# Non Json body
def test_post_plant_non_json_body():
    response = requests.post(base_url + "/plant", data="brate")
    response_json = response.json()

    assert response.status_code == 422
    assert response_json['detail'][0]['type'] == 'value_error.jsondecode'