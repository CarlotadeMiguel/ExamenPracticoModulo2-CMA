import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from app.config.setting import DevelopmentConfig
from app.extensions import db
from app.routes.tasks import tasks_bp

# Carga variables de entorno desde .env
load_dotenv()

def create_app():
    # Instancia la app
    app = Flask(__name__, instance_relative_config=False)

    # 1) Carga la configuración de desarrollo
    app.config.from_object(DevelopmentConfig)

    # 2) Forzar siempre SQLite en instance/app.db
    db_path = os.path.join(app.instance_path, 'app.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    os.makedirs(app.instance_path, exist_ok=True)
    if not os.path.exists(db_path):
        open(db_path, 'a').close()

    # 3) Habilitar CORS para todas las rutas
    CORS(app)

    # 4) Inicializar extensiones
    db.init_app(app)

    # 5) Crear todas las tablas definidas en los modelos
    with app.app_context():
        db.create_all()

    # 6) Registrar blueprint de tareas
    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')

    return app
