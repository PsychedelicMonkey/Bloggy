import os
basedir = os.path.dirname(os.path.abspath(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'insert-secret-key'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.environ.get('IMAGE_UPLOADS') or 'app/static/user_uploads'
    BACKGROUND_IMAGES = os.environ.get('BACKGROUND_IMAGES') or 'app/static/images'
    ALLOWED_FILE_EXTENSIONS = ['jpeg', 'jpg', 'png', 'gif']