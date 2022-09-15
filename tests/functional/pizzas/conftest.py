import asyncio
import uuid
from dataclasses import asdict, dataclass
from typing import Callable

import pytest
from faker import Faker
from fastapi.testclient import TestClient
from pytest_bdd import given, parsers, when
from requests import Response

from pizzeria.pizza.infrastructure.models import Pizzas
from pizzeria.system.strawberry.types import from_global_id, to_global_id

from ..conftest import execute_graphql_query


@dataclass
class PizzaFixture:
    """Pizza fixture."""

    id: str
    name: str
    toppings: list[str]
    price: int


@pytest.fixture
def make_pizza(faker: Faker) -> Callable[[], PizzaFixture]:
    """Build a random pizza fixture."""

    def __make_pizza() -> PizzaFixture:
        _id = to_global_id("PizzaNode", str(uuid.uuid4()))
        _name = faker.name()
        _price = faker.random.choice(
            [
                1099,
                1199,
                1299,
                1399,
                1499,
                1599,
            ]
        )
        _toppings = faker.random_choices(
            elements=[
                "pepperoni",
                "mushroom",
                "cheese",
                "sausage",
                "onion",
                "black olives",
                "basil",
                "mozzarella",
                "bacon",
                "ham",
            ]
        )

        return PizzaFixture(id=_id, name=_name, price=_price, toppings=_toppings)

    return __make_pizza


@pytest.fixture
def pizzas_query() -> str:
    """Graphql pizzas query."""
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


@pytest.fixture
def pizza_query() -> str:
    """Graphql pizza query."""
    return """
      query Pizza($pizzaId: ID!) {
        pizza(id: $pizzaId) {
          id
          name
          price
          toppings
        }
      }
    """


@pytest.fixture
def add_pizza_mutation() -> str:
    """Graphql add pizza muttation."""
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
                code
                path
              }
              ... on Error {
                message
                code
                path
              }
            }
          }
        }
    """


@given(parsers.cfparse('there are a pizza "{name}" in the menu'), target_fixture="pizza")
def there_are_a_pizza_in_the_menu(
    make_pizza: Callable[[], PizzaFixture],
    client: TestClient,  # pylint: disable=unused-argument
    event_loop: asyncio.AbstractEventLoop,
    name: str,
) -> PizzaFixture:
    """There are a pizza in the menu."""
    pizza = make_pizza()
    pizza.name = name

    async def save_pizza() -> Pizzas:
        return await Pizzas.create(
            id=uuid.UUID(from_global_id(pizza.id)),
            name=pizza.name,
            price=pizza.price,
            toppings=pizza.toppings,
        )

    event_loop.run_until_complete(save_pizza())

    return pizza


@when("I want to sell it", target_fixture="response")
def i_want_to_sell_it(client: TestClient, pizza: PizzaFixture, add_pizza_mutation: str) -> Response:
    """I want to sell it."""
    variables = {"input": asdict(pizza)}

    response = execute_graphql_query(client, add_pizza_mutation, variables)

    return response
