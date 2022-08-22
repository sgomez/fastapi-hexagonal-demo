from typing import Any, Dict

from fastapi import FastAPI
from tortoise.backends.base.config_generator import generate_config
from tortoise.contrib.fastapi import register_tortoise

from .settings import MODULES, config


def register_orm(
    app: FastAPI,
    database_url: str,
    generate_schemas: bool = False,
) -> None:
    register_tortoise(
        app,
        db_url=database_url,
        modules={"models": MODULES},
        generate_schemas=generate_schemas,
        add_exception_handlers=True,
    )


ENV = generate_config(
    db_url=config.database_url,
    app_modules={"modules": MODULES},
)
