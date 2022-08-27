from typing import Callable

from hamcrest import assert_that, equal_to
from pytest_bdd import given, parsers, scenario, then
from requests import Response

from pizzeria.pizza.ports.graphql.mutations.add_pizza import NameAlreadyExistsError

from ..matchers import error_in_response
from .conftest import PizzaFixture


@scenario("pizzas/pizza_unique_name_validation.feature", "Cannot add a pizza with a duplicated name")
def test_cannot_add_a_pizza_with_a_duplicated_name() -> None:
    """Cannot add a pizza with a duplicated name."""


@given(parsers.parse('I want to create another pizza "{name:w}"'), target_fixture="pizza")
def i_want_to_create_another_pizza_margherita(
    make_pizza: Callable[[], PizzaFixture], name: str
) -> PizzaFixture:
    """I want to create another pizza "margherita"."""
    pizza = make_pizza()
    pizza.name = name

    return pizza


@then("I get a duplicated name error")
def i_get_a_duplicated_name_error(response: Response) -> None:
    """I get a duplicated name error."""
    assert_that(response.status_code, equal_to(200))
    assert_that(NameAlreadyExistsError, error_in_response(response))
