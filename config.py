import os
from dotenv import load_dotenv

basedir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'insert-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    POSTS_PER_PAGE = 15

    UPLOAD_FOLDER = os.environ.get('IMAGE_UPLOADS') or os.path.join(basedir, 'images/')
    BACKGROUND_IMAGES = os.environ.get('BACKGROUND_IMAGES') or 'app/static/images'
    ALLOWED_FILE_EXTENSIONS = ['jpeg', 'jpg', 'png', 'gif']

    UNSPLASH_ACCESS_KEY = os.environ.get('UNSPLASH_ACCESS_KEY')
    UNSPLASH_SECRET_KEY = os.environ.get('UNSPLASH_SECRET_KEY')
    UNSPLASH_APP_NAME = os.environ.get('UNSPLASH_APP_NAME')