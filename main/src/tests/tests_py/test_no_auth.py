import uvicorn
import pytest
import requests

from datetime import datetime


base_url = "http://127.0.0.1:8080"


def get_temp_name(name):
    return datetime.today().strftime('%Y-%m-%d-%H:%M:%S:%mm') + name    


####################################
###########  PLANT  ################
####################################


##################
##### GET  

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
    assert response.status_code == 200
    response_json = response.json()
    print(response_json)
    assert response_json['latin_name'] == plant_name
    assert response_json['common_name'][0] == 'commonname1'
    assert response_json['common_name'][1] == 'commonname420'
    assert response_json['metadata']['bra'] == 'te'
    assert response_json['metadata']['te'] == 'bra'



##################
##### POST  

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
    assert response.status_code == 422

    response_json = response.json()
    print(response_json)
    assert response_json['detail'][0]['loc'][1] == 'latin_name'


# Missing both parameters
def test_plant_post_empty_param():
    data = ' '
    response = requests.post(base_url + "/plant", json=data)
    assert response.status_code == 422

    response_json = response.json()
    print(response_json)
    assert response_json['detail'][0]['loc'][1] == 'latin_name'


# Non Json body
def test_plant_post_non_json_body():
    response = requests.post(base_url + "/plant", data="brate")
    assert response.status_code == 422



# Get nonexisting plant
def test_plant_get_non_existing():
    response = requests.get(base_url + "/plant/gucciguccilouislousfendifendiprada")
    assert response.status_code == 404

    response_json = response.json()
    assert response_json["detail"] == 'Object does not exist'



##################
#####  PUT  

# Update data of a plant
def test_put_plant():
    plant_name = get_temp_name("test_put_plant")

    common_name1 = 'common_name1'
    common_name2 = 'common_name420'
    meta1_key = 'kekekekekekeke'
    meta2_key = 'tektje#$Qkwjk'
    meta1_value = "fkjdslfskdflj"
    meta2_value = "1240912iwejlfkjw"

    # create

    data = {'latin_name': plant_name, 
            'common_name': [common_name1, common_name2],
            'metadata': {meta1_key: meta1_value, meta2_key: meta2_value}}

    response = requests.post(base_url + "/plant", json=data)
    assert response.status_code == 200

    response_json = response.json()
    assert response_json['latin_name'] == plant_name
    assert response_json['common_name'][0] == common_name1
    assert response_json['common_name'][1] == common_name2
    assert response_json['metadata'][meta1_key] == meta1_value
    assert response_json['metadata'][meta2_key] == meta2_value

    # put

    meta1_value = 'value3 value2 value1'
    meta2_value = 'value2 value2 value2'
    common_name1 = 'krkrkrkrrkrkrkrkrkrkrkrkrkrkrk'

    data = {'common_name': [common_name1, common_name2],
            'metadata': {meta1_key: meta1_value, meta2_key: meta2_value}}
    response = requests.put(base_url + "/plant/" + plant_name, json=data)
    assert response.status_code == 200

    response_json = response.json()
    print(response_json)

    assert response_json['latin_name'] == plant_name
    assert response_json['common_name'][0] == common_name1
    assert response_json['common_name'][1] == common_name2
    assert response_json['metadata'][meta1_key] == meta1_value
    assert response_json['metadata'][meta2_key] == meta2_value



####################################
###########  AUTH  ################
####################################

username_key = 'username'
first_name_key = 'firstName'
last_name_key = 'lastName'
email_key = 'email'
password_key = 'password'
refresh_token_key = 'refresh_token'
access_token_key = 'access_token'
detail_key = 'detail'


def get_temp_user(id):
    username = get_temp_name('username') + id
    first_name = get_temp_name('fistName') + id
    last_name = get_temp_name('lastName') + id
    email = get_temp_name('email') + id + "@gmail.com"
    password = "password123" # damn secure

    data = {username_key: username, 
            first_name_key: first_name,
            last_name_key: last_name,
            email_key: email,
            password_key: password
            }

    return data


# Refresh token
def test_auth_refresh():
    data = get_temp_user('0')

    response = requests.post(base_url + "/auth/register", json=data)
    assert response.status_code != 200
    


# Register
def test_auth_register():
    data = get_temp_user('1')

    response = requests.post(base_url + "/auth/register", json=data)
    assert response.status_code != 200
    