from dataclasses import dataclass
from typing import List, Optional, Protocol
from uuid import UUID

from pizzeria.system.bus import Handler, Query

from ..domain.model import PizzaName

# region results


@dataclass(frozen=True)
class PizzaQueryResult:
    id: UUID
    name: str
    price: int
    toppings: list[str]


@dataclass(frozen=True)
class PizzasQueryResult:
    pizzas: list[PizzaQueryResult]


# endregion results


# region finder


class PizzaFinder(Protocol):
    async def find_all(self) -> List[PizzaQueryResult]:
        raise NotImplementedError

    async def find_by_name(self, name: PizzaName) -> Optional[PizzaQueryResult]:
        raise NotImplementedError


# endregion


# region get_pizzas


@dataclass(frozen=True)
class GetPizzasQuery(Query):
    ...


class GetPizzasQueryHandler(Handler[GetPizzasQuery, PizzasQueryResult]):
    def __init__(self, finder: PizzaFinder) -> None:
        self.__finder = finder

    async def handle(self, message: GetPizzasQuery) -> PizzasQueryResult:
        pizzas = await self.__finder.find_all()

        return PizzasQueryResult(pizzas=pizzas)


# endregion get_pizzas


# region get_pizza


@dataclass(frozen=True)
class GetPizzaQuery(Query):
    id: UUID


@dataclass(frozen=True)
class GetPizzaQueryResponse:
    pizza: Optional[PizzaQueryResult]


class GetPizzaQueryHandler(Handler[GetPizzaQuery, GetPizzaQueryResponse]):
    def __init__(self, finder: PizzaFinder) -> None:
        self.__finder = finder

    async def handle(self, message: GetPizzaQuery) -> GetPizzaQueryResponse:
        pizza = await self.__finder.find_all()

        return GetPizzaQueryResponse(pizza=pizza[0])


# endregion get_pizza
