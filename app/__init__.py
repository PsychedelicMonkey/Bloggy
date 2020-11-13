from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from config import Config

import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
moment = Moment(app)
login.login_view = 'auth.login'

from app.auth import auth
app.register_blueprint(auth, url_prefix='/auth')

from app.errors import error
app.register_blueprint(error)

from app.user import bp as bp
app.register_blueprint(bp, url_prefix='/user')

from app.uploads import upload
app.register_blueprint(upload)

from app.unsplash import unsplash
app.register_blueprint(unsplash)

from app import routes, models, forms

if not app.debug:
    if app.config['MAIL_SERVER']:
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'],
            subject='Bloggy Error'
        )
        mail_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/bloggy.log', maxBytes=20480, backupCount=10)
    file_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Bloggy startup')