from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'auth.login'

from app.auth import auth
app.register_blueprint(auth, url_prefix='/auth')

from app.uploads import upload
app.register_blueprint(upload)

from app import routes, models, forms