from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'passwrd'
# app.config['SQLALCHEMY_DATABASE_URI'] = ''

# db = SQLAlchemy(app)
# login_manager = LoginManager()
# login_manager.init_app(app)

from main import routes