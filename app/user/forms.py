from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired


class AboutMeForm(FlaskForm):
    text = TextAreaField('About Me', validators=[DataRequired()])
    submit = SubmitField('Save Changes')


class SendMessageForm(FlaskForm):
    recipient = StringField('Recipient:', validators=[DataRequired()])
    body = TextAreaField('Message:', validators=[DataRequired()])
    submit = SubmitField('Send message')