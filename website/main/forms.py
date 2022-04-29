from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError, Regexp, InputRequired, Email, EqualTo
from .models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    email = StringField('Email *', validators=[DataRequired(), Email()])
    password = PasswordField('password *', validators=[DataRequired()]) #, Regexp('^(?=.*\d).{6,8}$', message='Your password should be between 6 and 8 Charaters long and contain at least 1 number')])
    confirm_password = PasswordField('Confirm password *', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
       email = User.query.filter_by(email=email.data).first()
       if email:
           raise ValidationError('Email already Used. Please Use a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email *', validators=[DataRequired(), Email()])
    password = PasswordField('Password *', validators=[DataRequired(), ]) # Regexp('^(?=.*\d).{6,8}$', message='Your password should be between 6 and 8 Charaters long and contain at least 1 number')
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')