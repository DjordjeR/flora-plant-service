import requests
import time
from datetime import datetime

base_url = "http://127.0.0.1:8080"

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


# Search random plant and wait some time for results to appear
def test_plant():
  search = 'Polygonella polygama'
  params = {'q': search, 'limit': 20, 'offset': 0}
  response = requests.get(base_url + "/search", params=params)
  assert response.status_code == 200
  
  response_json = response.json()
  print(response_json)
  assert len(response_json[hits_key]) == 0

  # now wait 40s to results appear
  time.sleep(40)

  response = requests.get(base_url + "/search", params=params)
  assert response.status_code == 200
  
  response_json = response.json()
  print(response_json)
  assert len(response_json[hits_key]) != 0

