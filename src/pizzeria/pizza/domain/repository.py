from abc import ABC, abstractmethod

from result import Result

from .errors import PizzaNotFoundError
from .model import Pizza, PizzaId


class PizzaRepository(ABC):
    """Pizza repository interface."""

    @abstractmethod
    async def save(self, pizza: Pizza) -> None:
        """Save a pizza entity in the repository."""
        raise NotImplementedError

    @abstractmethod
    async def get(self, pizza_id: PizzaId) -> Result[Pizza, PizzaNotFoundError]:
        """Get a pizza entity from the repository."""
        raise NotImplementedError
