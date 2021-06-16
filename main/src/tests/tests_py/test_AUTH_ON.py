import requests
import time


######
###### Defined helpers
######

base_url = "http://127.0.0.1:8080"

username_key = 'username'
first_name_key = 'firstName'
last_name_key = 'lastName'
email_key = 'email'
password_key = 'password'
refresh_token_key = 'refresh_token'
access_token_key = 'access_token'

token_header_key = 'Authorization'
access_token = ' '
refresh_token = ' '

def get_temp_name(name):
    return str(time.time()) + name 

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


######
###### Defined tests
######

def plant_get():
    headers = {token_header_key: 'Bearer ' + access_token}
    response = requests.get(base_url + "/plant", headers=headers)
    assert response.status_code == 200


def plant_get_certain():
    headers = {token_header_key: 'Bearer ' + access_token}
    plant_name = get_temp_name("test_plant_get_certain")
    data = {'latin_name': plant_name, 
            'common_name': ['commonname1', 'commonname420'],
            'metadata': {'bra':'te', 'te':'bra'}}
    response = requests.post(base_url + "/plant", json=data, headers=headers)
    assert response.status_code == 200
    
    response = requests.get(base_url + "/plant/" + plant_name, headers=headers)
    assert response.status_code == 200
    response_json = response.json()
    print(response_json)
    assert response_json['latin_name'] == plant_name
    assert response_json['common_name'][0] == 'commonname1'
    assert response_json['common_name'][1] == 'commonname420'
    assert response_json['metadata']['bra'] == 'te'
    assert response_json['metadata']['te'] == 'bra'


def plant_post_duplicate():
    headers = {token_header_key: 'Bearer ' + access_token}
    plant_name = get_temp_name("test_plant_post_duplicate")
    data = {'latin_name': plant_name, 
            'common_name': ['commonname1', 'commonname420'],
            'metadata': {'bra':'te', 'te':'bra'}}
    response = requests.post(base_url + "/plant", json=data, headers=headers)
    assert response.status_code == 200


    data = {'latin_name': plant_name}
    response = requests.post(base_url + "/plant", json=data, headers=headers)
    assert response.status_code == 422


def plant_post_missing_latin_name():
    headers = {token_header_key: 'Bearer ' + access_token}
    data = {'common_name': ['commonname1', 'commonname420'],
            'metadata': {'bra':'te', 'te':'bra'}}
    response = requests.post(base_url + "/plant", json=data, headers=headers)
    assert response.status_code == 422

    response_json = response.json()
    print(response_json)
    assert response_json['detail'][0]['loc'][1] == 'latin_name'


def plant_post_empty_param():
    headers = {token_header_key: 'Bearer ' + access_token}
    data = ' '
    response = requests.post(base_url + "/plant", json=data, headers=headers)
    assert response.status_code == 422

    response_json = response.json()
    print(response_json)
    assert response_json['detail'][0]['loc'][1] == 'latin_name'


def plant_post_non_json_body():
    headers = {token_header_key: 'Bearer ' + access_token}
    response = requests.post(base_url + "/plant", data="brate", headers=headers)
    assert response.status_code == 422


def plant_get_non_existing():
    headers = {token_header_key: 'Bearer ' + access_token}
    response = requests.get(base_url + "/plant/gucciguccilouislousfendifendiprada", headers=headers)
    assert response.status_code == 404

    response_json = response.json()
    assert response_json["detail"] == 'Object does not exist'

def put_plant():
    headers = {token_header_key: 'Bearer ' + access_token}
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

    response = requests.post(base_url + "/plant", json=data, headers=headers)
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
    response = requests.put(base_url + "/plant/" + plant_name, json=data, headers=headers)
    assert response.status_code == 200

    response_json = response.json()
    print(response_json)

    assert response_json['latin_name'] == plant_name
    assert response_json['common_name'][0] == common_name1
    assert response_json['common_name'][1] == common_name2
    assert response_json['metadata'][meta1_key] == meta1_value
    assert response_json['metadata'][meta2_key] == meta2_value


######
###### Get token first
######

def test_and_get_auth_token():
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

    global access_token 
    access_token = response_json[access_token_key]

    global refresh_token
    refresh_token = response_json[refresh_token_key]


######
###### Run tests with aquired token
######

##### GET  

# Get available plants
def test_plant_get():
    plant_get()

# Get certain plant
def test_plant_get_certain():
    plant_get_certain()

##### POST  

# Try to create a duplicate
def test_plant_post_duplicate():
    plant_post_duplicate()

# Missing latin_name parameter
def test_plant_post_missing_latin_name():
    plant_post_missing_latin_name()

# Missing both parameters
def test_plant_post_empty_param():
    plant_post_empty_param()

# Non Json body
def test_plant_post_non_json_body():
    plant_post_non_json_body()

# Get nonexisting plant
def test_plant_get_non_existing():
    plant_get_non_existing()

#####  PUT  

# Update data of a plant
def test_put_plant():
    put_plant()



######
###### Refresh token and run same tests again with the new token
######

def test_token_refresh():
    data = {refresh_token_key: refresh_token}
    response = requests.post(base_url + "/auth/refresh", json=data)
    assert response.status_code == 200

    response_json = response.json()
    assert len(response_json.keys()) == 7

    global access_token
    access_token = response_json[access_token_key]



def test_refreshed_plant_get():
    plant_get()

def test_refreshed_plant_get_certain():
    plant_get_certain()

def test_refreshed_plant_post_duplicate():
    plant_post_duplicate()

def test_refreshed_plant_post_missing_latin_name():
    plant_post_missing_latin_name()

def test_refreshed_plant_post_empty_param():
    plant_post_empty_param()

def test_refreshed_plant_post_non_json_body():
    plant_post_non_json_body()

def test_refreshed_plant_get_non_existing():
    plant_get_non_existing()

def test_refreshed_put_plant():
    put_plant()