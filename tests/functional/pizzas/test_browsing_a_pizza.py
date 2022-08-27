"""Browsing pizzas feature tests."""

from dataclasses import asdict
from functools import partial
from uuid import uuid4

import pytest_bdd
from fastapi.testclient import TestClient
from hamcrest import assert_that, equal_to
from pytest_bdd import parsers, then, when
from requests import Response

from pizzeria.system.strawberry.types import to_global_id

from ..conftest import execute_graphql_query
from .conftest import PizzaFixture

scenario = partial(pytest_bdd.scenario, "pizzas/browsing_a_pizza.feature")


@scenario("Browse one pizza details")
def test_browse_one_pizza_details() -> None:
    """Browse one pizza details."""


@scenario("Browse one pizza that does not exists")
def test_browse_one_pizza_that_does_not_exists() -> None:
    """Browse one pizza that does not exists."""


@when(parsers.cfparse("I want to browse it"), target_fixture="response")
def i_want_to_browse_a_pizza(client: TestClient, pizza: PizzaFixture, pizza_query: str) -> Response:
    """I want to browse a pizza."""
    variables = {"pizzaId": pizza.id}

    return execute_graphql_query(client, pizza_query, variables)


@when("I want to browse a pizza than does not exists", target_fixture="response")
def i_want_to_browse_a_pizza_than_does_not_exists(client: TestClient, pizza_query: str) -> Response:
    """I want to browse a pizza than does not exists."""
    variables = {"pizzaId": to_global_id("PizzaNode", str(uuid4()))}

    return execute_graphql_query(client, pizza_query, variables)


@then("I see its details")
def i_see_its_details(pizza: PizzaFixture, response: Response) -> None:
    """I see its details."""
    content = response.json()

    assert_that(response.status_code, equal_to(200))
    assert_that(content["data"]["pizza"], equal_to(asdict(pizza)))


@then("I see the pizza does not exist")
def i_see_the_pizza_does_not_exist(response: Response):
    """I see the pizza does not exist."""

    content = response.json()

    assert_that(response.status_code, equal_to(200))
    assert_that(content["data"]["pizza"], equal_to(None))
