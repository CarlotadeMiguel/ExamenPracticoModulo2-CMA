# backend/app/__init__.py
from flask import Flask
from .config.setting import DevelopmentConfig
from .routes.tasks import tasks_bp          

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    app.register_blueprint(tasks_bp, url_prefix='/api')  

    return app
