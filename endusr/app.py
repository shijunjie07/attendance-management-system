from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import *





app = Flask(__name__, instance_relative_config=True)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECRET_KEY'] = SECRET_KEY

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance_system_v0.db'  # Change this to your database URI
# app.config['SECRET_KEY'] = 'supersecretkey'
# app = Flask(__name__, instance_relative_config=True)
# app.config.from_pyfile('../config.py')

db = SQLAlchemy()
db.init_app(app)

migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# from backend_app import routes, models  # Assuming you have a separate routes and models file
from .routes import *


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)




# # # backend_app/app.py
# # # webapp_demo/app.py




# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
# from config import SQLALCHEMY_DATABASE_URL, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY

# db = SQLAlchemy()
# login_manager = LoginManager()

# def create_app():
#     app = Flask(__name__, instance_relative_config=True)
#     app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URL
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
#     app.config['SECRET_KEY'] = SECRET_KEY
#     db.init_app(app)
#     login_manager.init_app(app)

#     with app.app_context():
#         from . import models  # Import models to register them with SQLAlchemy
#         db.create_all()

#     return app

