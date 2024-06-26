# ---------------------------------
# config
# @author: Shi Junjie A178915
# Sat 8 June 2024
# ---------------------------------

import os

# SQLALCHEMY_DATABASE_URI = 'sqlite:///attendance_system_v0.db'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'attendance.db')
SQLALCHEMY_DATABASE_URL = f'sqlite:///{DB_PATH}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.urandom(24)