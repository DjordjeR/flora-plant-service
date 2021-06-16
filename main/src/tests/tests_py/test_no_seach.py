from requests.api import get
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


hits_key = 'hits'


# Random search where the result should be empty
def test_random_search():
    search = 'acacia'
    params = {'q': search, 'limit': 20, 'offset': 0}
    response = requests.get(base_url + "/search", params=params)
    assert response.status_code == 200
    
    response_json = response.json()
    print(response_json)
    assert len(response_json[hits_key]) == 0
