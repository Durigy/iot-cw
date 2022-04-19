from . import db, login_manager, app, bcrypt
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.String(20), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)