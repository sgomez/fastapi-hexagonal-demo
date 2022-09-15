"""Browsing pizzas feature tests."""

from fastapi.testclient import TestClient
from hamcrest import assert_that, equal_to, has_length
from pytest_bdd import given, parsers, scenario, then, when
from requests import Response

from ..conftest import execute_graphql_query


@scenario("pizzas/browsing_pizzas.feature", "Browse available pizzas")
def test_browse_available_pizzas() -> None:
    """Browse available pizzas."""


@scenario("pizzas/browsing_pizzas.feature", "There are no pizzas in the menu")
def test_there_are_no_pizzas_in_the_menu() -> None:
    """There are no pizzas in the menu."""


@given("there are no pizzas in the menu")
def there_are_no_pizzas_in_the_menu() -> None:
    """There are no pizzas in the menu."""


@when("I want to browse all available pizzas", target_fixture="response")
def i_want_to_browse_all_available_pizzas(client: TestClient, pizzas_query: str) -> Response:
    """I want to browse all available pizzas."""
    return execute_graphql_query(client, pizzas_query)


@then(parsers.parse("I see {count:d} pizzas"))
def i_see_n_pizzas(response: Response, count: int = 0) -> None:
    """I see N pizzas."""
    content = response.json()

    assert_that(response.status_code, equal_to(200))
    assert_that(content["data"]["pizzas"], has_length(count))


@then("I see there are no pizzas")
def i_see_there_are_no_pizzas(response: Response) -> None:
    """I see there are no pizzas."""
    content = response.json()

    assert_that(response.status_code, equal_to(200))
    assert_that(content["data"]["pizzas"], has_length(0))
