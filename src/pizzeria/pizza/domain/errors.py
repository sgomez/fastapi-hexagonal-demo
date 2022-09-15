from pizzeria.system.domain.errors import LogicDomainError, ValidationError

# region RuleDomainError


class InvalidPizzaIdError(ValidationError):
    """Invalid pizza id error."""

    def __init__(self) -> None:
        super().__init__(message="The id is not valid", label="id", code="pizza_id_invalid")


class EmptyPizzaNameError(ValidationError):
    """Empty pizza name error."""

    def __init__(self) -> None:
        super().__init__(message="The name is not valid", label="name", code="pizza_name_invalid")


class InvalidLengthPizzaNameError(ValidationError):
    """Pizza name too long."""

    def __init__(self, max_length: int) -> None:
        super().__init__(
            message=f"The name cannot be longer than {max_length} characters",
            label="name",
            code="pizza_name_too_long",
        )


class FewPizzaToppingsError(ValidationError):
    """Few toppings in the pizza."""

    def __init__(self) -> None:
        super().__init__(
            message="At least two topping are required", label="toppings", code="few_pizza_toppings"
        )


class InvalidPizzaToppingNameError(ValidationError):
    """Topping name too short o too long."""

    def __init__(self, name: str) -> None:
        super().__init__(
            message=f"Invalid topping name: [{name}]", label="toppings", code="pizza_topping_invalid"
        )


class CrimeAgainstHumanityError(ValidationError):
    """Topping name too short o too long."""

    def __init__(self) -> None:
        super().__init__(message="Are you crazy?", label="toppings", code="pinneapple_topping")


class NotIntegerPriceError(ValidationError):
    """Not valid price type."""

    def __init__(self) -> None:
        super().__init__(message="The price is not valid", label="price", code="pizza_price_invalid")


class NegativePriceError(ValidationError):
    """Pizza price cannot be free or negative."""

    def __init__(self) -> None:
        super().__init__(message="The price must be positive", label="price", code="pizza_price_non_positive")


# endregion

# region LogicDomainError


class PizzaNotFoundError(LogicDomainError):
    """Duplicate pizza id error."""

    def __init__(self, pizza_id: str) -> None:
        super().__init__(f"Pizza with id {pizza_id} not found", "pizza_id", "pizza_not_found")


class DuplicatedPizzaIdError(LogicDomainError):
    """Duplicate pizza id error."""

    def __init__(self, pizza_id: str) -> None:
        super().__init__(f"Duplicated id {pizza_id}", "pizza_id", "pizza_duplicated_id")


class DuplicatedNameError(LogicDomainError):
    """Duplicate pizza name error."""

    def __init__(self, name: str) -> None:
        super().__init__(f"Duplicated name {name}", "name", "pizza_duplicated_name")


# endregion
