from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '2d921c3ffbb0137b9b8e287c6a5c2ee78251c11b97973faf'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/iot'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://qume_iot_user:dasQuLHW8pC6CR8@localhost:3306/qume_iot_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from . import routes