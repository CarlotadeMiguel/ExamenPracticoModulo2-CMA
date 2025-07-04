# backend/migrations/env.py

from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config, pool
from alembic import context

# Carga variables de entorno (.flaskenv y .env)
from dotenv import load_dotenv
load_dotenv()

# Importa la aplicación y la configuración de SQLAlchemy
from app import create_app, db

# Crea la app para leer su configuración
app = create_app()
config = context.config

# Sobrescribe la URL de la base de datos con la de app.config
config.set_main_option('sqlalchemy.url', app.config['SQLALCHEMY_DATABASE_URI'])

# Configura el logging
fileConfig(config.config_file_name)

# Metadatos de los modelos
target_metadata = db.metadata

def run_migrations_offline():
    """Corre migraciones en modo offline (sin conexión)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Corre migraciones en modo online (con conexión)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
