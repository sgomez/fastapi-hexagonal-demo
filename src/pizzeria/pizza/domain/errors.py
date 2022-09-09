from pizzeria.system.domain.errors import LogicDomainError, ValidationError


class DuplicatedNameError(LogicDomainError):
    def __init__(self, name: str) -> None:
        super().__init__(f"Duplicated name {name}", "name", "pizza_duplicated_name")


class InvalidPizzaIdError(ValidationError):
    def __init__(self) -> None:
        super().__init__(message="The id is not valid", label="id", code="pizza_id_invalid")


class EmptyPizzaNameError(ValidationError):
    def __init__(self) -> None:
        super().__init__(message="The name is not valid", label="name", code="pizza_name_invalid")


class InvalidLengthPizzaNameError(ValidationError):
    def __init__(self, max_length: int) -> None:
        super().__init__(
            message=f"The name cannot be longer than {max_length} characters",
            label="name",
            code="pizza_name_too_long",
        )


class FewPizzaToppingsError(ValidationError):
    def __init__(self) -> None:
        super().__init__(
            message="At least two topping are required", label="toppings", code="few_pizza_toppings"
        )


class InvalidPizzaToppingNameError(ValidationError):
    def __init__(self, name: str) -> None:
        super().__init__(
            message=f"Invalid topping name: [{name}]", label="toppings", code="pizza_topping_invalid"
        )


class NotIntegerPriceError(ValidationError):
    def __init__(self) -> None:
        super().__init__(message="The price is not valid", label="price", code="pizza_price_invalid")


class NegativePriceError(ValidationError):
    def __init__(self) -> None:
        super().__init__(message="The price must be positive", label="price", code="pizza_price_non_positive")
