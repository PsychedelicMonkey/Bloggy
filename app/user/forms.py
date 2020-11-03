from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class AboutMeForm(FlaskForm):
    text = TextAreaField('About Me', validators=[DataRequired()])
    submit = SubmitField('Save Changes')