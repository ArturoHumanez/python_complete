import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

from src.lab_7.models import Base

# Añadimos la raíz del proyecto al path para que encuentre 'src'
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # 1. Obtenemos la ruta absoluta al archivo .db de forma dinámica
    # Estamos en: src/lab_7/migrations/env.py
    # Queremos: src/lab_7/test.db
    base_path = Path(__file__).resolve().parent.parent
    db_file = base_path / "test.db"

    # Construimos la URL de SQLAlchemy para Windows
    # sqlite:///C:\Ruta\test.db
    db_url = f"sqlite:///{db_file}"

    # 2. Obtenemos la configuración del archivo .ini
    config_dict = config.get_section(config.config_ini_section, {})

    # 3. SOBREESCRIBIMOS la URL del .ini con nuestra ruta dinámica
    config_dict["sqlalchemy.url"] = db_url

    connectable = engine_from_config(
        config_dict,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
