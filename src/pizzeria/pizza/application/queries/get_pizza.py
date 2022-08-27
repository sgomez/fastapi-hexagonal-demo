from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from pizzeria.system.bus import Handler, Query

from ..dto import PizzaDTO
from ..services import PizzaFinder


@dataclass(frozen=True)
class GetPizzaQuery(Query):
    id: UUID


@dataclass(frozen=True)
class GetPizzaQueryResult:
    pizza: Optional[PizzaDTO]


class GetPizzaQueryHandler(Handler[GetPizzaQuery, GetPizzaQueryResult]):
    def __init__(self, finder: PizzaFinder) -> None:
        self.__finder = finder

    async def handle(self, message: GetPizzaQuery) -> GetPizzaQueryResult:
        pizza = await self.__finder.find(message.id)

        return GetPizzaQueryResult(pizza=pizza)
