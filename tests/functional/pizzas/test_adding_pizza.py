"""Add a pizza feature tests."""

from dataclasses import asdict
from functools import partial
from typing import Callable

import pytest_bdd
from fastapi.testclient import TestClient
from hamcrest import assert_that, equal_to, has_item
from pytest_bdd import given, parsers, scenario, then

from ..conftest import execute_graphql_query
from .conftest import PizzaFixture

scenario = partial(pytest_bdd.scenario, "pizzas/adding_pizza.feature")


@scenario("Add a new pizza")
def test_add_a_new_pizza():
    """Add a new pizza."""


@given(
    parsers.cfparse(
        'the pizza "{name}" has next toppings: {toppings:Topping+}', extra_types={"Topping": str}
    ),
    target_fixture="pizza",
)
def the_pizza_has_next_toppings(
    make_pizza: Callable[[], PizzaFixture], name: str, toppings: list[str]
) -> PizzaFixture:
    """The pizza has next toppings."""
    pizza = make_pizza()
    pizza.name = name
    pizza.toppings = toppings

    return pizza


@then("it will be available in the menu")
def it_will_available_in_the_menu(client: TestClient, pizza: PizzaFixture, pizzas_query: str) -> None:
    """It will be available in the menu."""

    response = execute_graphql_query(client, pizzas_query)
    content = response.json()

    assert_that(response.status_code, equal_to(200))
    assert_that(content["data"]["pizzas"], has_item(asdict(pizza)))
