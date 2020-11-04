from flask import Blueprint

unsplash = Blueprint('unsplash', __name__)

from app.unsplash import routes