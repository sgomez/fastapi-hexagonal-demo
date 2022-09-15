from uuid import UUID

from hamcrest import assert_that, is_

from ..errors import EmptyPizzaNameError, FewPizzaToppingsError, InvalidPizzaIdError, NegativePriceError
from ..model import Pizza, PizzaFactory


def test_build_pizza() -> None:
    """Test to build a pizza."""
    # Arrange
    pizza_id = UUID("e50dbd3f-e915-4edb-8d13-7f5ff6dddd67")

    # Act
    result = PizzaFactory.build(str(pizza_id), "Margharita", 1200, ["mozzarella", "basil"])

    # Assert
    assert_that(result.unwrap(), is_(Pizza))


def test_build_pizza_with_errors() -> None:
    """Test to build a pizza with errors."""
    # Arrange

    # Act
    result = PizzaFactory.build("no-id", "", 0, [])

    # Assert
    assert_that(result.unwrap_err(), is_(list))
    assert_that(result.unwrap_err()[0], is_(InvalidPizzaIdError))
    assert_that(result.unwrap_err()[1], is_(EmptyPizzaNameError))
    assert_that(result.unwrap_err()[2], is_(NegativePriceError))
    assert_that(result.unwrap_err()[3], is_(FewPizzaToppingsError))
