import secrets
import os


class Config:
    SECRET_KEY = secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'profile_pics')
    UPLOAD_POST_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'post_pics')