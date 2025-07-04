# backend/app/__init__.py
import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from .config.setting import DevelopmentConfig

# Cargar variables de entorno de .env
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Crear app usando la carpeta 'instance/' por defecto (junto a run.py)
    app = Flask(__name__, instance_relative_config=True)

    # 1) Cargar configuración base
    app.config.from_object(DevelopmentConfig)

    # 2) Forzar la URI absoluta de SQLite en backend/instance/app.db
    db_path = os.path.join(app.instance_path, 'app.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

    # 3) Asegurar existencia de carpeta 'instance/' y fichero 'app.db'
    os.makedirs(app.instance_path, exist_ok=True)
    if not os.path.exists(db_path):
        open(db_path, 'a').close()

    # 4) Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # 5) Registrar blueprint de tareas
    from .routes.tasks import tasks_bp
    app.register_blueprint(tasks_bp)

    return app
