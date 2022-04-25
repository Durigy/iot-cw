from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '35ae3b45dacdca9eefdc2f657004b9512bfbab4416d9ab44'
app.config['SQLALCHEMY_DATABASE_URI'] = ''

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from . import routes