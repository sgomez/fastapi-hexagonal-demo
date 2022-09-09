from dataclasses import dataclass
from typing import Any, ClassVar
from uuid import UUID

from result import Err, Ok, Result, as_result

from pizzeria.system.domain.errors import DomainError

from .errors import (
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
    value: UUID

    def __post_init__(self) -> None:
        if not isinstance(self.value, UUID) or self.value.version != 4:
            raise InvalidPizzaIdError

    @as_result(DomainError)
    @staticmethod
    def from_string(value: str) -> "PizzaId":
        try:
            return PizzaId(value=UUID(value))
        except ValueError as err:
            raise InvalidPizzaIdError from err

    @as_result(DomainError)
    @staticmethod
    def new(value: UUID) -> "PizzaId":
        return PizzaId(value=value)


@dataclass(frozen=True)
class PizzaName:
    MAX_LENGTH: ClassVar[int] = 60

    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str) or len(self.value) == 0:
            raise EmptyPizzaNameError

        if not 0 < len(self.value) <= self.MAX_LENGTH:
            raise InvalidLengthPizzaNameError(self.MAX_LENGTH)

    @as_result(DomainError)
    @staticmethod
    def new(value: str) -> "PizzaName":
        return PizzaName(value=value)


@dataclass(frozen=True)
class PizzaPrice:
    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int):
            raise NotIntegerPriceError

        if self.value <= 0:
            raise NegativePriceError

    @as_result(DomainError)
    @staticmethod
    def new(value: int) -> "PizzaPrice":
        return PizzaPrice(value=value)


@dataclass(frozen=True)
class PizzaToppings:
    values: list[str]

    def __post_init__(self) -> None:
        if len(self.values) < 2:
            raise FewPizzaToppingsError

        for topping in self.values:
            if not 0 < len(topping) < 25:
                raise InvalidPizzaToppingNameError(topping)

    @as_result(DomainError)
    @staticmethod
    def new(values: list[str]) -> "PizzaToppings":
        return PizzaToppings(values=values)


class Pizza:
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
        return self.__pizza_id

    @property
    def name(self) -> PizzaName:
        return self.__name

    @property
    def price(self) -> PizzaPrice:
        return self.__price

    @property
    def toppings(self) -> PizzaToppings:
        return self.__toppings


class PizzaFactory:
    @staticmethod
    def build(pizza_id: str, name: str, price: int, toppings: list[str]) -> Result[Pizza, list[DomainError]]:
        values: dict[str, Result[Any, DomainError]] = {
            "pizza_id": PizzaId.from_string(pizza_id),
            "name": PizzaName.new(name),
            "price": PizzaPrice.new(price),
            "toppings": PizzaToppings.new(toppings),
        }

        errors = [value.unwrap_err() for value in values.values() if value.is_err()]

        if errors:
            return Err(errors)

        return Ok(Pizza(**{key: value.unwrap() for key, value in values.items()}))
