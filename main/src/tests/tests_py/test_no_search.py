import time
import requests
from datetime import datetime

base_url = "http://127.0.0.1:8080"

def get_temp_name(name):
    return datetime.today().strftime('%Y-%m-%d-%H:%M:%S:%mm') + name    

hits_key = 'hits'


# This should fail as no search service is running
def test_no_search():
    search = 'acacia'
    params = {'q': search, 'limit': 20, 'offset': 0}
    response = requests.get(base_url + "/search", params=params)
    assert response.status_code == 200

    response_json = response.json()
    print(response_json)
    assert len(response_json[hits_key]) == 0

    # now wait 20s to results appear
    time.sleep(20)
    
    response_json = response.json()
    print(response_json)
    assert len(response_json[hits_key]) == 0


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


def check_user_data(data, response_json):
    assert response_json[username_key] == data[username_key]
    assert response_json[first_name_key] == data[first_name_key]
    assert response_json[last_name_key] == data[last_name_key]
    assert response_json[email_key] == data[email_key]


# Get token
def test_auth_token():

    # register 
    data = get_temp_user('0')

    response = requests.post(base_url + "/auth/register", json=data)
    assert response.status_code == 200
    
    response_json = response.json()
    print(response_json)
    assert len(response_json.keys()) == 5
    check_user_data(data, response_json)

    # token

    data = {username_key: data[username_key],
            password_key: data[password_key]
    }

    response = requests.post(base_url + "/auth/token", json=data)
    assert response.status_code == 200
    
    response_json = response.json()
    print(response_json)
    assert len(response_json.keys()) == 7



# Refresh token
def test_auth_refresh():

    # register
    data = get_temp_user('1')

    response = requests.post(base_url + "/auth/register", json=data)
    assert response.status_code == 200
    
    response_json = response.json()
    print(response_json)

    assert len(response_json.keys()) == 5
    check_user_data(data, response_json)

    # get token

    data = {username_key: data[username_key],
            password_key: data[password_key]
    }

    response = requests.post(base_url + "/auth/token", json=data)
    assert response.status_code == 200
    
    response_json = response.json()
    print(response_json)
    assert len(response_json.keys()) == 7
    refresh_token = response_json[refresh_token_key]

    # refresh token

    data = {refresh_token_key: refresh_token}
    response = requests.post(base_url + "/auth/refresh", json=data)
    assert response.status_code == 200
    assert len(response_json.keys()) == 7


# Register
def test_auth_register():

    data = get_temp_user('2')
    
    response = requests.post(base_url + "/auth/register", json=data)
    assert response.status_code == 200
    
    response_json = response.json()
    print(response_json)
    assert len(response_json.keys()) == 5
    check_user_data(data, response_json)


# Double register
def test_auth_double_register():

    data = get_temp_user('3')

    response = requests.post(base_url + "/auth/register", json=data)
    assert response.status_code == 200
    
    response_json = response.json()
    print(response_json)
    assert len(response_json.keys()) == 5
    check_user_data(data, response_json)


    response = requests.post(base_url + "/auth/register", json=data)
    assert response.status_code == 401
    
    response_json = response.json()
    print(response_json)
    assert response_json['detail'] == 'User already exists.'
    
    