"""Pizza validation feature tests."""

from functools import partial
from typing import Callable

import pytest_bdd
from faker import Faker
from hamcrest import assert_that, equal_to
from pytest_bdd import given, parsers, then
from requests import Response

from pizzeria.system.strawberry.errors import ValidationError

from ..matchers import error_in_response
from .conftest import PizzaFixture

scenario = partial(pytest_bdd.scenario, "pizzas/pizza_validation.feature")


@scenario("Trying to add a pizza with a long name")
def test_trying_to_add_a_pizza_with_a_long_name() -> None:
    """Trying to add a pizza with a long name."""


@scenario("Trying to add a pizza with an empty name")
def test_trying_to_add_a_pizza_with_an_empty_name() -> None:
    """Trying to add a pizza with an empty name."""


@given(
    parsers.parse("I want to add a pizza with a name longer than {length:d} characters"),
    target_fixture="pizza",
)
def i_want_to_add_a_pizza_with_a_name_longer_than_n_characters(
    make_pizza: Callable[[], PizzaFixture],
    faker: Faker,
    length: int,
) -> PizzaFixture:
    """I want to add a pizza with a name longer than N characters."""
    pizza = make_pizza()
    pizza.name = faker.pystr(min_chars=length, max_chars=length)

    return pizza


@given("I want to add a pizza with an empty name", target_fixture="pizza")
def i_want_to_add_a_pizza_with_an_empty_name(
    make_pizza: Callable[[], PizzaFixture],
) -> PizzaFixture:
    """I want to add a pizza with an empty name."""
    pizza = make_pizza()
    pizza.name = ""

    return pizza


@then("I get a invalid name error")
def i_get_a_invalid_name_error(response: Response) -> None:
    """I get a invalid name error."""
    assert_that(response.status_code, equal_to(200))
    assert_that(ValidationError, error_in_response(response))
