from app import app
from app.unsplash import unsplash

import requests

URL = 'https://api.unsplash.com/photos'
CLIENT = '?client_id={}'.format(app.config['UNSPLASH_ACCESS_KEY'])

def get_random():
    call = '{}/random/{}'.format(URL, CLIENT)
    response = requests.get(call)
    if response.status_code == 200:
        photo = response.json()
        return photo