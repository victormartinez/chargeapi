from typing import Dict

from decouple import config

# Database specifications
DB_USER = config("DB_USER", "")
DB_PASS = config("DB_PASS", "")
DB_HOST = config("DB_HOST", "")
DB_PORT = config("DB_PORT", default="5432")
DB_NAME = config("DB_NAME", "")
DB_POOL_SIZE = config(
    "DB_POOL_SIZE", cast=int, default=50
)
DB_MAX_OVERFLOW = config(
    "DB_MAX_OVERFLOW", cast=int, default=10
)
DB_ECHO = config(
    "DB_ECHO", cast=bool, default=False
)
DB_EXPIRE_ON_COMMIT = config(
    "DB_EXPIRE_ON_COMMIT", cast=bool, default=False
)
DB_AUTOCOMMIT = config(
    "DB_AUTOCOMMIT", cast=bool, default=False
)
DB_AUTOFLUSH = config(
    "DB_AUTOFLUSH", cast=bool, default=False
)
DB_POOL_PRE_PING = config("DB_POOL_PRE_PING", cast=bool, default=False)


def build_database_uri() -> str:
    # As alembic.ini needs separated DB vars, we can't return SQLALCHEMY_DATABASE_URI directly.
    # genesis/alembic/env.py:28

    return f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def build_engine_config() -> Dict[str, str]:
    return {
        'pool_size': DB_POOL_SIZE,
        'max_overflow': DB_MAX_OVERFLOW,
        'echo': DB_ECHO,
        'pool_pre_ping': DB_POOL_PRE_PING
    }


def build_session_config() -> Dict[str, bool]:
    return {
        'expire_on_commit': DB_EXPIRE_ON_COMMIT,
        'autocommit': DB_AUTOCOMMIT,
        'autoflush': DB_AUTOFLUSH,
    }
