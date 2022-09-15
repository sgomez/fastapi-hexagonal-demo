import asyncio
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
    """Application event loop fixture."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def client(event_loop: asyncio.BaseEventLoop) -> Iterator[TestClient]:
    """Application test client fixture."""
    initializer(MODULES, loop=event_loop)
    with TestClient(__app_test) as c:
        yield c
    finalizer()


def execute_graphql_query(
    client: TestClient, query: str, variables: Optional[Dict[str, Any]] = None
) -> Response:
    """Execute a request to the graphql endpoint."""
    data: Dict[str, Any] = {"query": query}

    if variables:
        data["variables"] = variables

    return client.post("/graphql", json=data)
