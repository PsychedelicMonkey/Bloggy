from flask import render_template
from flask_login import login_required
from app import app
from app.forms import EmptyForm
from app.unsplash import unsplash

import json
import requests

URL = 'https://api.unsplash.com/photos'
CLIENT = '?client_id={}'.format(app.config['UNSPLASH_ACCESS_KEY'])

def get_random():
    call = '{}/random/{}&count=30'.format(URL, CLIENT)
    response = requests.get(call)
    if response.status_code == 200:
        photo = response.json()
        return photo


@unsplash.route('/random', methods=['GET', 'POST'])
@login_required
def random():
    form = EmptyForm()
    if form.validate_on_submit():
        photos = get_random()
        #photos = json.loads(open('results.json').read())
        '''result = {
            "photo": photo['urls']['small'],
            "user": photo['user']['username'],
            "link": photo['user']['links']['html']
        }'''
        return render_template('unsplash/result.html', photos=photos)
    else:
        return 'Test'