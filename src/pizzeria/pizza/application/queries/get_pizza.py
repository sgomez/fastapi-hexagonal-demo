from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from result import Ok, Result

from pizzeria.system.bus import Handler, Query
from pizzeria.system.domain.errors import DomainError

from ..dto import PizzaDTO
from ..services import PizzaFinder


@dataclass(frozen=True)
class GetPizzaQuery(Query):
    """Get pizza query."""

    id: UUID


@dataclass(frozen=True)
class GetPizzaQueryResult:
    """Get pizza result."""

    pizza: Optional[PizzaDTO]


class GetPizzaQueryHandler(Handler[GetPizzaQuery, GetPizzaQueryResult]):
    """Get pizza query handler."""

    def __init__(self, finder: PizzaFinder) -> None:
        self.__finder = finder

    async def handle(self, message: GetPizzaQuery) -> Result[GetPizzaQueryResult, list[DomainError]]:
        """Handle a GetPizzaQuery message."""
        pizza = await self.__finder.find(message.id)

        return Ok(GetPizzaQueryResult(pizza=pizza))
