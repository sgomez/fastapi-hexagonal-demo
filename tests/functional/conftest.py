import asyncio
from dataclasses import asdict, dataclass
from typing import Any, Dict, Iterator, Optional

import pytest
from fastapi.testclient import TestClient
from requests import Response
from tortoise.contrib.test import finalizer, initializer

from pizzeria.kernel import Kernel
from pizzeria.system.container import container
from pizzeria.system.settings import MODULES, test_config

__app_test = Kernel(config=test_config).boot()
container(__app_test)


@pytest.fixture(scope="function")
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def client(event_loop: asyncio.BaseEventLoop) -> Iterator[TestClient]:
    initializer(MODULES, loop=event_loop)
    with TestClient(__app_test) as c:
        yield c
    finalizer()


@dataclass
class PizzaFixture:
    id: str
    name: str
    toppings: list[str]
    price: int


def execute_graphql_query(client: TestClient, query: str, input: Optional[Any] = None) -> Response:
    data: Dict[str, Any] = {"query": query}

    if input:
        data["variables"] = {"input": asdict(input)}

    return client.post("/graphql", json=data)
