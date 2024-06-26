from .app import db, login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.String(10), primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_lecturer = db.Column(db.Boolean, default=False)

    def __init__(self, id, email, password, is_lecturer=False):
        self.id = id
        self.email = email
        self.password = password
        self.is_lecturer = is_lecturer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)