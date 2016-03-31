from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired
import settings

class LoginForm(Form):
    accesskey = PasswordField('Access Key', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class CreateIssue(Form):
    title = StringField('Title', validators=[DataRequired()])
    if settings.redmine:
        redmine = StringField('Redmine', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])