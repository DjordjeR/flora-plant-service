import uvicorn
import pytest
import requests
import time

from app.main import get_application
from multiprocessing import Process
from datetime import datetime


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
#####  GET  ######
##################


# Get available plants
def test_plant_get():
    response = requests.get(base_url + "/plant")
    assert response.status_code == 200


# Get certain plant
def test_plant_get_certain():
    temp_plant_name = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

    data = {'common_name': temp_plant_name, 'latin_name': temp_plant_name}
    response = requests.post(base_url + "/plant", json=data)
    assert response.status_code == 200

    response = requests.get(base_url + "/plant/" + temp_plant_name)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["common_name"] == temp_plant_name
    assert response_json['latin_name'] == temp_plant_name
    assert response_json['metadata'] == None



##################
#####  POST  #####
##################

# Try to create a duplicate
def test_plant_post_duplicate():
    temp_plant_name = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

    data = {'common_name': temp_plant_name, 'latin_name': temp_plant_name}
    response = requests.post(base_url + "/plant", json=data)
    print(response.json())
    assert response.status_code == 200

    data = {'common_name': temp_plant_name, 'latin_name': temp_plant_name}
    response = requests.post(base_url + "/plant", json=data)

    assert response.status_code == 422


# Missing common_name parameter
def test_plant_post_missing_common_name():
    data = {'latin_name': 'gucci'}
    response = requests.post(base_url + "/plant", json=data)

    response_json = response.json()
    assert response.status_code == 422
    assert response_json['detail'][0]['loc'][1] == 'common_name'
   

# Missing latin_name parameter
def test_plant_post_missing_latin_name():
    data = {'common_name': 'gucci'}
    response = requests.post(base_url + "/plant", json=data)

    response_json = response.json()
    assert response.status_code == 422
    assert response_json['detail'][0]['loc'][1] == 'latin_name'


# Missing both parameters
def test_plant_post_missing_latin_name():
    data = ' '
    response = requests.post(base_url + "/plant", json=data)

    response_json = response.json()
    assert response.status_code == 422
    assert response_json['detail'][0]['loc'][1] == 'common_name'
    assert response_json['detail'][1]['loc'][1] == 'latin_name'


# Non Json body
def test_plant_post_non_json_body():
    response = requests.post(base_url + "/plant", data="brate")

    response_json = response.json()
    assert response.status_code == 422
    assert response_json['detail'][0]['type'] == 'value_error.jsondecode'


# Get nonexisting plant
def test_plant_get_non_existing():
    response = requests.get(base_url + "/plant/gucciguccilouislousfendifendiprada")

    response_json = response.json()
    assert response.status_code == 404
    assert response_json["detail"] == 'Object does not exist'



##################
#####  PUT  ######
##################

# Try to create a duplicate
def test_put_plant():
    temp_plant_name = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

    data = {'common_name': temp_plant_name, 'latin_name': temp_plant_name}
    response = requests.post(base_url + "/plant", json=data)
    assert response.status_code == 200




    data = {'common_name': temp_plant_name, 'latin_name': temp_plant_name}
    response = requests.post(base_url + "/plant", json=data)

    assert response.status_code == 422