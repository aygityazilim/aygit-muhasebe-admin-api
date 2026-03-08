import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from dotenv import load_dotenv
import sys
sys.dont_write_bytecode = True
# --- Load .env early ---
base_dir = os.path.dirname(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, ".env"))

# --- Append project root to sys.path ---
sys.path.append(base_dir)

# --- Import project-specific modules ---
from shared.db import AdminBase
from shared.config import Config
from shared.models import UserModel
# --- Alembic Config ---
config = context.config

# Use dynamic URL from environment/config instead of hardcoding
database_url = Config.ADMIN_DATABASE_REAL_URL

if not database_url:
    raise Exception("DATABASE_URL is not set!")

config.set_main_option("sqlalchemy.url", database_url)

# --- Logging config ---
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Metadata for autogenerate ---
target_metadata = AdminBase.metadata
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
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
