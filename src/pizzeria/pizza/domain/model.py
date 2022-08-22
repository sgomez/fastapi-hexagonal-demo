from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class PizzaId:
    value: UUID

    def __post_init__(self):
        if not isinstance(self.value, UUID):
            raise RuntimeError("PizzaId must be a UUID")

    @staticmethod
    def fromString(id: str) -> "PizzaId":
        return PizzaId(value=UUID(id))


@dataclass(frozen=True)
class PizzaName:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise RuntimeError("PizzaName must be a string")

        if 0 >= len(self.value) >= 100:
            raise RuntimeError("PizzaName invalid name")


@dataclass(frozen=True)
class PizzaPrice:
    value: int

    def __post_init__(self):
        if not isinstance(self.value, int):
            raise RuntimeError("PizzaPrice must be an integer")

        if self.value <= 0:
            raise RuntimeError("PizzaPrice must be positive")


@dataclass(frozen=True)
class PizzaToppings:
    values: list[str]

    def __post_init__(self):
        for topping in self.values:
            if 0 >= len(topping) >= 25:
                raise RuntimeError("Invalid topping name")


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
