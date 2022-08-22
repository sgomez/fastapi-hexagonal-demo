import asyncio
import uuid

import pytest
from fastapi.testclient import TestClient
from pytest_bdd import given, parsers, scenario, then, when

from pizzeria.pizza.infrastructure.models import Pizzas
from pizzeria.system.strawberry.types import to_global_id

from ..conftest import PizzaFixture, execute_graphql_query


@pytest.fixture(scope="module")
def query() -> str:
    return """
        query Pizzas {
          pizzas {
            id
            name
            price
            toppings
          }
        }
    """


@pytest.fixture(scope="module")
def mutation() -> str:
    return """
        mutation AddPizza($input: PizzaInput!) {
          addPizza(input: $input) {
            pizza {
              id
              name
              price
              toppings
            }
            errors {
              __typename
              ... on NameAlreadyExistsError {
                message
                path
              }
              ... on UserError {
                message
                path
              }
            }
          }
        }
    """


@scenario("pizzas/pizza_unique_name_validation.feature", "Cannot add a pizza with a duplicated name")
def test_cannot_add_a_pizza_with_a_duplicated_name():
    """Cannot add a pizza with a duplicated name."""


@given(parsers.cfparse('there are a pizza "{name:w}" in the menu'))
def there_are_a_pizza_in_the_menu(client: TestClient, event_loop: asyncio.AbstractEventLoop, name: str):
    """there are a pizza "margherita" in the menu."""

    async def save_pizza():
        await Pizzas.create(id=uuid.uuid4(), name=name, price=1000, toppings=[])

    event_loop.run_until_complete(save_pizza())


@when(parsers.cfparse('I want to add another pizza "{name:w}"'), target_fixture="errors")
def i_want_to_add_another_pizza_margherita(client: TestClient, name: str, mutation: str):
    """I want to add another pizza "margherita"."""
    _id = to_global_id("PizzaNode", str(uuid.uuid4()))

    pizza = PizzaFixture(id=_id, name=name, price=1000, toppings=[])
    response = execute_graphql_query(client, mutation, pizza)
    content = response.json()

    assert response.status_code == 200, response.text
    assert content["data"]["addPizza"]["errors"], response.text

    return content["data"]["addPizza"]["errors"]


@then("I get a duplicated name error")
def i_get_a_duplicated_name_error(errors: dict):
    """I get a duplicated name error."""

    assert errors[0]["__typename"] == "NameAlreadyExistsError", errors
