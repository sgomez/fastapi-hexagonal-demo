from dataclasses import dataclass

from result import Ok, Result

from pizzeria.system.bus import Handler, Query
from pizzeria.system.domain.errors import DomainError

from ..dto import PizzasDTO
from ..services import PizzaFinder


@dataclass(frozen=True)
class GetPizzasQuery(Query):
    """Get pizzas query."""


@dataclass(frozen=True)
class GetPizzasQueryResult:
    """Get pizzas result."""

    pizzas: PizzasDTO


class GetPizzasQueryHandler(Handler[GetPizzasQuery, GetPizzasQueryResult]):
    """Get pizzas query handler."""

    def __init__(self, finder: PizzaFinder) -> None:
        self.__finder = finder

    async def handle(self, message: GetPizzasQuery) -> Result[GetPizzasQueryResult, list[DomainError]]:
        """Handle GetPizzasQuery message."""
        pizzas = await self.__finder.find_all()

        return Ok(GetPizzasQueryResult(pizzas=pizzas))
