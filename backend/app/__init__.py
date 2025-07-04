# backend/app/__init__.py
import os
from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS 
from .config.setting import DevelopmentConfig

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key')

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.tasks import tasks_bp
    app.register_blueprint(tasks_bp, url_prefix='/api')
    return app
