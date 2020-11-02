from flask import Flask

app = Flask(__name__)

from app.auth import auth
app.register_blueprint(auth, url_prefix='/auth')

from app import routes