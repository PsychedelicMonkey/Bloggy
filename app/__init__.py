from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app.auth import auth
app.register_blueprint(auth, url_prefix='/auth')

from app import routes