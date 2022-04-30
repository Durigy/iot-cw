from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta
from flask_restful import Api

app = Flask(__name__)

app.config['SECRET_KEY'] = '2d921c3ffbb0137b9b8e287c6a5c2ee78251c11b97973faf'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/iot'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://qume_iot_user:dasQuLHW8pC6CR8@localhost:3306/qume_iot_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=1)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

api = Api(app)

from . import routes