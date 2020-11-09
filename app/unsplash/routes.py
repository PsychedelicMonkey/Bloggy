from flask import render_template, jsonify
from flask_login import login_required, current_user
from app import app, db
from app.forms import EmptyForm
from app.models import File
from app.user.forms import DownloadPhotoForm
from app.unsplash import unsplash

import os
import json
import requests
import urllib.request

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
        download = DownloadPhotoForm()
        return render_template('unsplash/result.html', photos=photos, form=download)
    else:
        return 'Test'


@unsplash.route('/download/<id>', methods=['POST'])
@login_required
def download(id):
    form = DownloadPhotoForm()
    if form.validate_on_submit():
        link = URL + '/' + id + '/download' + CLIENT
        request = requests.get(link)
        if request.status_code == 200:
            photoUrl = request.json()
            name = id + '.jpg'
            photo = File(name=name, user=current_user, file_author=form.user.data, file_author_url=form.user_url.data)
            urllib.request.urlretrieve(photoUrl['url'], os.path.join(app.config['UPLOAD_FOLDER'], name))
            db.session.add(photo)
            db.session.commit()
            return 'Your photo is downloaded'
        else:
            return 'There was a problem downloading your photo'
    else:
        return render_template(url_for('index'))