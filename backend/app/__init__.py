# backend/app/__init__.py
import os
from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config.setting import DevelopmentConfig

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.tasks import tasks_bp
    app.register_blueprint(tasks_bp, url_prefix='/api')
    return app
