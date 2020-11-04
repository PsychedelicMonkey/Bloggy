from flask import Blueprint
from app import app

upload = Blueprint('upload', __name__, static_folder=app.config['UPLOAD_FOLDER'])

from app.uploads import routes, forms