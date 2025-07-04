#backend/app/__init__.py
from flask import Flask
from .config.setting import DevelopmentConfig

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    return app
