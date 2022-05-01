from datetime import datetime
from . import db, login_manager
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.String(20), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    api_key = db.Column(db.String(20), unique=True, nullable=False)

# Relationships #
    device = db.relationship('Device', backref = 'user', lazy = True, foreign_keys = 'Device.user_id')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Device(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_armed  = db.Column(db.Boolean, nullable = True, default = False)

# Links (ForeignKeys) #
    user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable = False)

# Relationships #
    device_data = db.relationship('DeviceInfo', backref = 'device', lazy = True, foreign_keys = 'DeviceInfo.device_id')


class DeviceInfo(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    time = db.Column(db.DateTime, nullable = True, default = datetime.utcnow)
    light = db.Column(db.Boolean, nullable = True)
    is_intruder = db.Column(db.Boolean, nullable = True)
    reset_counter = db.Column(db.Integer, nullable = True)

# Links (ForeignKeys) #
    device_id = db.Column(db.String(20), db.ForeignKey('device.id'), nullable = False)