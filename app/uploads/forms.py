from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import FileField, SubmitField
from app import app


class UploadFileForm(FlaskForm):
    file = FileField('File', validators=[FileRequired(), FileAllowed(app.config['ALLOWED_FILE_EXTENSIONS'])])
    submit = SubmitField('Upload')