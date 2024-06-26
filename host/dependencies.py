from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import *

db = SQLAlchemy()
app = Flask(__name__, instance_relative_config=True)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECRET_KEY'] = SECRET_KEY
db.init_app(app)