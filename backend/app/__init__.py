# backend/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))

    app = Flask(__name__)
    app.config.from_object(os.getenv('FLASK_ENV') == 'development'
        and "app.config.setting.DevelopmentConfig"
        or "app.config.setting.Config"
    )

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.tasks import tasks_bp
    app.register_blueprint(tasks_bp, url_prefix='/api')

    return app
