# ---------------------------------
# app
# @author: Shi Junjie A178915
# Sat 9 June 2024
# ---------------------------------

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# from .models import db, Course, Class, Attendance, Lecturer, Device, \
#     Student, course_student, course_lecturer

from .dependencies import app

from .routes import *

# app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URL
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
# app.config['SECRET_KEY'] = SECRET_KEY
# db.init_app(app)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# db.init_app(app)

device_status = {}
mock_classes = {}
ESP_DEVICES = []

APP_SERVER_PORT = 5001
CHECK_INTERVAL = 600  # seconds
from .device_manager import start_status_check_thread



if __name__ == '__main__':
    from .sql_handler import SQLHandler
    sql_handler = SQLHandler()
    start_status_check_thread(sql_handler, CHECK_INTERVAL)
    app.run(debug=True, host='0.0.0.0', port=APP_SERVER_PORT)

# # # # backend_app/app.py
# # # from flask import Flask
# # # from flask_sqlalchemy import SQLAlchemy
# # # from config import SQLALCHEMY_DATABASE_URL, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY

# # # db = SQLAlchemy()

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from config import SQLALCHEMY_DATABASE_URL, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY

# app = Flask(__name__, instance_relative_config=True)
# db = SQLAlchemy()

# def create_app():
#     app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URL
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
#     app.config['SECRET_KEY'] = SECRET_KEY
#     db.init_app(app)

#     with app.app_context():
#         from . import models  # Import models to register them with SQLAlchemy
#         db.create_all()

#     return app
