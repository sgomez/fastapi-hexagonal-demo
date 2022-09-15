from typing import Optional, Protocol
from uuid import UUID

from .dto import PizzaDTO, PizzasDTO


class PizzaFinder(Protocol):
    """Interface to search pizzas from read model."""

    async def find_all(self) -> PizzasDTO:
        """Find all pizzas from read model."""
        raise NotImplementedError

    async def find(self, id: UUID) -> Optional[PizzaDTO]:
        """Find one pizza from read model."""
        raise NotImplementedError

    async def find_by_name(self, name: str) -> Optional[PizzaDTO]:
        """Find one pizza by name from read model."""
        raise NotImplementedError
