from dotenv import dotenv_values
from pydantic import BaseSettings
from tortoise.backends.base.config_generator import generate_config

__config = {
    **dotenv_values(".env"),
    **dotenv_values(".env.local"),
}

MODULES = [
    "pizzeria.pizza.infrastructure.models",
    "aerich.models",
]


class Settings(BaseSettings):
    host: str = "127.0.0.0"
    port: int = 8000
    reload: bool = False
    workers: int = 0
    debug: bool = False
    database_url: str = "sqlite://var/db/db.sqlite3"
    generate_schemas: bool = False

    class Config:
        env_file = None


config = Settings(**{k.lower(): v for k, v in __config.items()})
test_config = Settings(database_url="sqlite://:memory:", debug=True, generate_schemas=True)
