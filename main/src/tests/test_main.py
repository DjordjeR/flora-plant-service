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
    uvicorn.run(app, port=8000, loop="asyncio", lifespan="on")

@pytest.fixture
def server():
    proc = Process(target=run_server, args=(), daemon=True)
    proc.start() 
    yield
    proc.kill()


def get_temp_name(name):
    return datetime.today().strftime('%Y-%m-%d-%H:%M:%S:%mm') + name    

##################
#####  GET  ######
##################


# Get available plants
def test_plant_get():
    response = requests.get(base_url + "/plant")
    assert response.status_code == 200


# Get certain plant
def test_plant_get_certain():
    plant_name = get_temp_name("test_plant_get_certain")
    data = {'latin_name': plant_name, 
            'common_name': ['commonname1', 'commonname420'],
            'metadata': {'bra':'te', 'te':'bra'}}
    response = requests.post(base_url + "/plant", json=data)
    assert response.status_code == 200
    

    response = requests.get(base_url + "/plant/" + plant_name)
    response_json = response.json()
    print(response_json)
    assert response.status_code == 200
    assert response_json['latin_name'] == plant_name
    assert response_json['common_name'][0] == 'commonname1'
    assert response_json['common_name'][1] == 'commonname420'
    assert response_json['metadata']['bra'] == 'te'
    assert response_json['metadata']['te'] == 'bra'



##################
#####  POST  #####
##################

# Try to create a duplicate
def test_plant_post_duplicate():
    plant_name = get_temp_name("test_plant_post_duplicate")
    data = {'latin_name': plant_name, 
            'common_name': ['commonname1', 'commonname420'],
            'metadata': {'bra':'te', 'te':'bra'}}
    response = requests.post(base_url + "/plant", json=data)
    assert response.status_code == 200


    data = {'latin_name': plant_name}
    response = requests.post(base_url + "/plant", json=data)

    assert response.status_code == 422
   

# Missing latin_name parameter
def test_plant_post_missing_latin_name():
    data = {'common_name': ['commonname1', 'commonname420'],
            'metadata': {'bra':'te', 'te':'bra'}}
    response = requests.post(base_url + "/plant", json=data)

    response_json = response.json()
    print(response_json)
    assert response.status_code == 422
    assert response_json['detail'][0]['loc'][1] == 'latin_name'


# Missing both parameters
def test_plant_post_empty_param():
    data = ' '
    response = requests.post(base_url + "/plant", json=data)

    response_json = response.json()
    print(response_json)
    assert response.status_code == 422
    assert response_json['detail'][0]['loc'][1] == 'latin_name'


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

# Update data of a plant
def test_put_plant():
    plant_name = get_temp_name("test_put_plant")

    common_name1 = 'common_name1'
    common_name2 = 'common_name420'
    meta1_key = 'kekekekekekeke'
    meta2_key = 'tektje#$Qkwjk'
    meta1_value = "fkjdslfskdflj"
    meta2_value = "1240912iwejlfkjw"

    data = {'latin_name': plant_name, 
            'common_name': [common_name1, common_name2],
            'metadata': {meta1_key: meta1_value, meta2_key: meta2_value}}

    response = requests.post(base_url + "/plant", json=data)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['latin_name'] == plant_name
    assert response_json['common_name'][0] == common_name1
    assert response_json['common_name'][1] == common_name2
    assert response_json['metadata'][meta1_key] == meta1_value
    assert response_json['metadata'][meta2_key] == meta2_value


    meta1_value = 'value3 value2 value1'
    meta2_value = 'value2 value2 value2'
    #common_name1 = 'krkrkrkrrkrkrkrkrkrkrkrkrkrkrk'

    data = {'common_name': [common_name1, common_name2],
            'metadata': {meta1_key: meta1_value, meta2_key: meta2_value}}
    response = requests.put(base_url + "/plant/" + plant_name, json=data)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json['latin_name'] == plant_name
    assert response_json['common_name'][0] == common_name1
    assert response_json['common_name'][1] == common_name2
    assert response_json['metadata'][meta1_key] == meta1_value
    assert response_json['metadata'][meta2_key] == meta2_value