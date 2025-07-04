import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from app.config.setting import DevelopmentConfig
from app.extensions import db
from app.routes.tasks import tasks_bp

load_dotenv()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(DevelopmentConfig)

    # Override de la URI solo si NO estamos en testing
    if not app.config.get('TESTING', False):
        db_path = os.path.join(app.instance_path, 'app.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
        os.makedirs(app.instance_path, exist_ok=True)
        if not os.path.exists(db_path):
            open(db_path, 'a').close()

    CORS(app)
    db.init_app(app)

    # Crear tablas si NO es testing
    if not app.config.get('TESTING', False):
        with app.app_context():
            db.create_all()

    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
    return app
