from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, Regexp, InputRequired, Email
from .models import User
from flask_login import current_user

class LoginForm(FlaskForm):
    email = StringField('Email *', validators=[DataRequired(), Email()])
    password = PasswordField('Password *', validators=[DataRequired(), ]) # Regexp('^(?=.*\d).{6,8}$', message='Your password should be between 6 and 8 Charaters long and contain at least 1 number')
    submit = SubmitField('Login')