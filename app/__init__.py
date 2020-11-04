from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
moment = Moment(app)
login.login_view = 'auth.login'

from app.auth import auth
app.register_blueprint(auth, url_prefix='/auth')

from app.user import bp as bp
app.register_blueprint(bp, url_prefix='/user')

from app.uploads import upload
app.register_blueprint(upload)

from app.unsplash import unsplash
app.register_blueprint(unsplash)

from app import routes, models, forms