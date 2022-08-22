import uuid
from dataclasses import asdict

import pytest
from fastapi.testclient import TestClient
from pytest_assert_utils import assert_dict_is_subset
from pytest_bdd import given, parsers, scenario, then, when

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


@scenario("pizzas/add_pizza.feature", "Add a new pizza")
def test_add_a_new_pizza():
    """Add a new pizza."""


@given(
    parsers.cfparse(
        'the pizza "{name}" has next toppings: {toppings:Topping+}', extra_types={"Topping": str}
    ),
    target_fixture="pizza",
)
def the_pizza_has_next_toppings(name: str, toppings: list[str]) -> PizzaFixture:
    _id = to_global_id("PizzaNode", str(uuid.uuid4()))

    return PizzaFixture(id=_id, name=name, toppings=toppings, price=0)


@when(parsers.cfparse("I want to sell it at {price:d} euros"), target_fixture="pizza")
def i_want_to_sell_it(client: TestClient, pizza: PizzaFixture, price: int, mutation: str) -> PizzaFixture:
    """I want to sell it at 10 euros."""
    pizza.price = price * 100

    response = execute_graphql_query(client, mutation, pizza)
    content = response.json()

    assert response.status_code == 200, response.text
    assert content["data"]["addPizza"]["errors"] == [], response.text

    return pizza


@then("it will be available in the menu")
def it_will_available_in_the_menu(client: TestClient, pizza: PizzaFixture, query: str) -> None:
    """the "margherita" pizza is available in the menu."""

    response = execute_graphql_query(client, query)
    content = response.json()

    assert response.status_code == 200, response.text
    assert_dict_is_subset(asdict(pizza), content["data"]["pizzas"][0]), response.text
