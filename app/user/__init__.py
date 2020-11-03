from flask import Blueprint

# This blueprint is used for all the actions used for changing the user's information
bp = Blueprint('user', __name__)

from app.user import routes