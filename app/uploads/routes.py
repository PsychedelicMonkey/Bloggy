from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from app import app
from app.uploads import upload
from app.uploads.forms import UploadFileForm
from werkzeug.utils import secure_filename

import os

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_FILE_EXTENSIONS']


@upload.route('/upload_file', methods=['POST'])
@login_required
def upload_file():
    form = UploadFileForm()
    if form.validate_on_submit():
        if 'file' not in request.files:
            flash(u'No file was found!', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash(u'No selected file', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename('{}-{}'.format(current_user.username, file.filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(request.referrer)
    else:
        flash(u'Error', 'danger')
        return redirect(request.referrer)