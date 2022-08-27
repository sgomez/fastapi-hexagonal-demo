from dataclasses import dataclass

from pizzeria.system.bus import Handler, Query

from ..dto import PizzaDTO
from ..services import PizzaFinder


@dataclass(frozen=True)
class GetPizzasQuery(Query):
    ...


@dataclass(frozen=True)
class GetPizzasQueryResult:
    pizzas: list[PizzaDTO]


class GetPizzasQueryHandler(Handler[GetPizzasQuery, GetPizzasQueryResult]):
    def __init__(self, finder: PizzaFinder) -> None:
        self.__finder = finder

    async def handle(self, message: GetPizzasQuery) -> GetPizzasQueryResult:
        pizzas = await self.__finder.find_all()

        return GetPizzasQueryResult(pizzas=pizzas)
