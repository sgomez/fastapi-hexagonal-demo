from typing import List, Optional, Protocol
from uuid import UUID

from .dto import PizzaDTO


class PizzaFinder(Protocol):
    async def find_all(self) -> List[PizzaDTO]:
        raise NotImplementedError

    async def find(self, id: UUID) -> Optional[PizzaDTO]:
        raise NotImplementedError

    async def find_by_name(self, name: str) -> Optional[PizzaDTO]:
        raise NotImplementedError
