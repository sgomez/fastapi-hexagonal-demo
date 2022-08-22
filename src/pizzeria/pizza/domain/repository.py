from typing import Protocol
from uuid import UUID

from .model import Pizza


class PizzaRepository(Protocol):
    async def save(self, pizza: Pizza) -> None:
        raise NotImplementedError

    async def get(self) -> None:
        raise NotImplementedError
