from dataclasses import dataclass
from typing import Any, ClassVar
from uuid import UUID

from result import Err, Ok, Result, as_result

from pizzeria.system.domain.errors import DomainError

from .errors import (
    CrimeAgainstHumanityError,
    EmptyPizzaNameError,
    FewPizzaToppingsError,
    InvalidLengthPizzaNameError,
    InvalidPizzaIdError,
    InvalidPizzaToppingNameError,
    NegativePriceError,
    NotIntegerPriceError,
)


@dataclass(frozen=True)
class PizzaId:
    """Pizza identifier type."""

    value: UUID

    def __post_init__(self) -> None:
        """Validate input values."""
        if not isinstance(self.value, UUID) or self.value.version != 4:
            raise InvalidPizzaIdError

    @as_result(InvalidPizzaIdError)
    @staticmethod
    def from_string(value: str) -> "PizzaId":
        """Factory constructor."""
        try:
            return PizzaId(value=UUID(value))
        except ValueError as err:
            raise InvalidPizzaIdError from err

    @as_result(InvalidPizzaIdError)
    @staticmethod
    def new(value: UUID) -> "PizzaId":
        """Factory constructor."""
        return PizzaId(value=value)


@dataclass(frozen=True)
class PizzaName:
    """Pizza name type."""

    NAME_MAX_LENGTH: ClassVar[int] = 60

    value: str

    def __post_init__(self) -> None:
        """Validate input values."""
        if not isinstance(self.value, str) or len(self.value) == 0:
            raise EmptyPizzaNameError

        if not 0 < len(self.value) <= self.NAME_MAX_LENGTH:
            raise InvalidLengthPizzaNameError(self.NAME_MAX_LENGTH)

    @as_result(EmptyPizzaNameError, InvalidLengthPizzaNameError)
    @staticmethod
    def new(value: str) -> "PizzaName":
        """Factory constructor."""
        return PizzaName(value=value)


@dataclass(frozen=True)
class PizzaPrice:
    """Pizza price type."""

    value: int

    def __post_init__(self) -> None:
        """Validate input values."""
        if not isinstance(self.value, int):
            raise NotIntegerPriceError

        if self.value <= 0:
            raise NegativePriceError

    @as_result(NotIntegerPriceError, NegativePriceError)
    @staticmethod
    def new(value: int) -> "PizzaPrice":
        """Factory constructor."""
        return PizzaPrice(value=value)


@dataclass(frozen=True)
class PizzaToppings:
    """Pizza toppings type."""

    MINIMAL_TOPPINGS = 2
    NAME_MAX_LENGTH = 25
    FORBIDDEN_TOPPINGS = ["pineapple"]

    values: list[str]

    def __post_init__(self) -> None:
        """Validate input values."""
        if len(self.values) < self.MINIMAL_TOPPINGS:
            raise FewPizzaToppingsError

        for topping in self.values:
            if not 0 < len(topping) < self.NAME_MAX_LENGTH:
                raise InvalidPizzaToppingNameError(topping)
            if topping in self.FORBIDDEN_TOPPINGS:
                raise CrimeAgainstHumanityError

    @as_result(FewPizzaToppingsError, InvalidPizzaToppingNameError, CrimeAgainstHumanityError)
    @staticmethod
    def new(values: list[str]) -> "PizzaToppings":
        """Factory constructor."""
        return PizzaToppings(values=values)


class Pizza:
    """Pizza entity type."""

    __pizza_id: PizzaId
    __name: PizzaName
    __price: PizzaPrice
    __toppings: PizzaToppings

    def __init__(
        self,
        pizza_id: PizzaId,
        name: PizzaName,
        price: PizzaPrice,
        toppings: PizzaToppings,
    ) -> None:
        self.__pizza_id = pizza_id
        self.__name = name
        self.__price = price
        self.__toppings = toppings

    @property
    def id(self) -> PizzaId:
        """Get pizza id."""
        return self.__pizza_id

    @property
    def name(self) -> PizzaName:
        """Get pizza name."""
        return self.__name

    @property
    def price(self) -> PizzaPrice:
        """Get pizza price."""
        return self.__price

    @property
    def toppings(self) -> PizzaToppings:
        """Get pizza toppings."""
        return self.__toppings


class PizzaFactory:
    """Pizza factory."""

    @staticmethod
    def build(id: str | UUID, name: str, price: int, toppings: list[str]) -> Result[Pizza, list[DomainError]]:
        """Build a Pizza instance."""
        values: dict[str, Result[Any, DomainError]] = {
            "pizza_id": PizzaId.from_string(str(id)),
            "name": PizzaName.new(name),
            "price": PizzaPrice.new(price),
            "toppings": PizzaToppings.new(toppings),
        }

        errors = [value.unwrap_err() for value in values.values() if value.is_err()]

        if errors:
            return Err(errors)

        return Ok(Pizza(**{key: value.unwrap() for key, value in values.items()}))
