from flask import Blueprint

upload = Blueprint('upload', __name__)

from app.uploads import routes, forms