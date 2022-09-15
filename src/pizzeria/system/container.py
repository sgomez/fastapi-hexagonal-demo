from dataclasses import dataclass
from typing import Any

from fastapi import FastAPI, Request

from pizzeria.pizza.application.commands.add_pizza import AddPizzaCommand, AddPizzaCommandHandler
from pizzeria.pizza.application.queries.get_pizza import GetPizzaQuery, GetPizzaQueryHandler
from pizzeria.pizza.application.queries.get_pizzas import GetPizzasQuery, GetPizzasQueryHandler
from pizzeria.pizza.infrastructure.services import TortoisePizzaFinder, TortoisePizzaRepository

from .bus import Command, MessageBus, Query


@dataclass
class Container:
    """Container class."""

    command_bus: MessageBus[Any, None]
    query_bus: MessageBus[Any, Any]


def build_container() -> Container:
    """Container factory."""
    command_bus = MessageBus[Command, None]()
    query_bus = MessageBus[Query, Any]()

    container = Container(
        command_bus=command_bus,
        query_bus=query_bus,
    )

    pizza_repository = TortoisePizzaRepository()
    pizza_finder = TortoisePizzaFinder()

    container.command_bus.register_handler(
        AddPizzaCommand, AddPizzaCommandHandler(pizza_repository, pizza_finder)
    )
    container.query_bus.register_handler(GetPizzasQuery, GetPizzasQueryHandler(pizza_finder))
    container.query_bus.register_handler(GetPizzaQuery, GetPizzaQueryHandler(pizza_finder))

    return container


def container(app: FastAPI) -> FastAPI:
    """Container wrapper."""
    app.state.container = build_container()

    return app


def get_command_bus(request: Request) -> MessageBus[Command, None]:
    """Command bus wrapper used for FastAPI DI."""
    return __get_container(request).command_bus


def get_query_bus(request: Request) -> MessageBus[Query, Any]:
    """Query bus wrapper used for FastAPI DI."""
    return __get_container(request).query_bus


def __get_container(request: Request) -> Container:
    app = request.app

    assert isinstance(app, FastAPI)

    container = app.state.container

    assert isinstance(container, Container)

    return container
