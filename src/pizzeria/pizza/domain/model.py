from dataclasses import dataclass
from typing import ClassVar
from uuid import UUID

from pizzeria.system.domain.errors import ValidationError


@dataclass(frozen=True)
class PizzaId:
    value: UUID

    def __post_init__(self):
        if not isinstance(self.value, UUID) or self.value.version != 4:
            raise ValidationError(message="The id is not valid", label="id", code="pizza_id_invalid")

    @staticmethod
    def fromString(id_: str) -> "PizzaId":
        return PizzaId(value=UUID(id_))


@dataclass(frozen=True)
class PizzaName:
    MAX_LENGTH: ClassVar[int] = 60

    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise ValidationError(message="The name is not valid", label="name", code="pizza_name_invalid")

        if not 0 < len(self.value) <= self.MAX_LENGTH:
            raise ValidationError(
                message=f"The name cannot be longer than {self.MAX_LENGTH} characters",
                label="name",
                code="pizza_name_too_long",
            )


@dataclass(frozen=True)
class PizzaPrice:
    value: int

    def __post_init__(self):
        if not isinstance(self.value, int):
            raise ValidationError(message="The price is not valid", label="price", code="pizza_price_invalid")

        if self.value <= 0:
            raise ValidationError(
                message="The price must be positive", label="price", code="pizza_price_non_positive"
            )


@dataclass(frozen=True)
class PizzaToppings:
    values: list[str]

    def __post_init__(self):
        for topping in self.values:
            if not 0 < len(topping) < 25:
                raise ValidationError(
                    message="Invalid topping name", label="toppings", code="pizza_topping_invalid"
                )


class Pizza:
    __id: PizzaId
    __name: PizzaName
    __price: PizzaPrice
    __toppings: PizzaToppings

    def __init__(
        self,
        id: PizzaId,
        name: PizzaName,
        price: PizzaPrice,
        toppings: PizzaToppings,
    ) -> None:
        self.__id = id
        self.__name = name
        self.__price = price
        self.__toppings = toppings

    @property
    def id(self) -> PizzaId:
        return self.__id

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
    def build(id: str, name: str, price: int, toppings: list[str]) -> Pizza:
        return Pizza(
            id=PizzaId.fromString(id),
            name=PizzaName(name),
            price=PizzaPrice(price),
            toppings=PizzaToppings(toppings),
        )
