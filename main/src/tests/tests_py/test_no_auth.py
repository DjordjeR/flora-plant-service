from requests.api import get
import uvicorn
import pytest
import requests

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


def get_temp_user():
    username = get_temp_name('username')
    first_name = get_temp_name('fistName')
    last_name = get_temp_name('lastName')
    email = get_temp_name('email') + "@gmail.com"
    password = "password123" # damn secure

    data = {username_key: username, 
            first_name_key: first_name,
            last_name_key: last_name,
            email_key: email,
            password_key: password
            }

    return data


def check_error_response(response_json):
    assert response_json[detail_key] == "Undown error"


# Get token
def test_auth_token():

    # register 
    data = get_temp_user()

    response = requests.post(base_url + "/auth/register", json=data)
    assert response.status_code != 200
    
    response_json = response.json()
    print(response_json)
    assert len(response_json.keys()) == 1
    check_error_response(response_json)



# Refresh token
def test_auth_refresh():
    data = get_temp_user()

    response = requests.post(base_url + "/auth/register", json=data)
    assert response.status_code != 200
    
    response_json = response.json()
    print(response_json)

    assert len(response_json.keys()) == 1
    check_error_response(response_json)
    


# Register
def test_auth_register():
    data = get_temp_user()

    response = requests.post(base_url + "/auth/register", json=data)
    assert response.status_code != 200
    
    response_json = response.json()
    print(response_json)
    assert len(response_json.keys()) == 1
    check_error_response(response_json)
    