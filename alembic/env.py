"""Alembic configuration for database migrations"""

from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from app.config import config
from app.models.resource import Resource
from app.models.village import Village
from app.models.analysis import Analysis

# this is the Alembic Config object
config_alembic = context.config

# Interpret the config file for Python logging
if config_alembic.config_file_name is not None:
    fileConfig(config_alembic.config_file_name)

# set the sqlalchemy.url value from app config
config_alembic.set_main_option("sqlalchemy.url", config.DATABASE_URL)

# Model's MetaData object for 'autogenerate' support
from app.database import engine
target_metadata = Resource.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config_alembic.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config_alembic.get_section(config_alembic.config_ini_section)
    configuration["sqlalchemy.url"] = config.DATABASE_URL
    
    connectable = engine_from_config(
        configuration,
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
