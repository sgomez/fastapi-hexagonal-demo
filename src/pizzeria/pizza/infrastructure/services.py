from typing import Optional
from uuid import UUID

from result import Err, Ok, Result

from ..application.dto import PizzaDTO, PizzasDTO
from ..application.services import PizzaFinder
from ..domain import model
from ..domain.errors import PizzaNotFoundError
from ..domain.repository import PizzaRepository
from .models import PizzaModel, Pizzas


class TortoisePizzaRepository(PizzaRepository):
    """Implementation of the PizzaRepository using Tortoise ORM."""

    async def save(self, pizza: model.Pizza) -> None:
        """Save a pizza entity in the repository."""
        await Pizzas(
            id=pizza.id.value,
            name=pizza.name.value,
            price=pizza.price.value,
            toppings=pizza.toppings.values,
        ).save()

    async def get(self, pizza_id: model.PizzaId) -> Result[model.Pizza, PizzaNotFoundError]:
        """Get a pizza entity from the repository."""
        pizza = await PizzaModel.from_queryset(Pizzas.filter(id=pizza_id.value))

        if not pizza:
            return Err(PizzaNotFoundError(str(pizza_id.value)))

        return Ok(model.PizzaFactory.build(**pizza[0].dict()).unwrap())


class TortoisePizzaFinder(PizzaFinder):
    """Implementation of the PizzaFinder using Tortoise ORM."""

    async def find_all(self) -> PizzasDTO:
        """Find all pizzas from read model."""
        pizzas = await PizzaModel.from_queryset(Pizzas.all())

        return [PizzaDTO(**pizza.dict()) for pizza in pizzas]

    async def find(self, id: UUID) -> Optional[PizzaDTO]:
        """Find one pizza from read model."""
        pizza = await PizzaModel.from_queryset(Pizzas.filter(id=id))

        if not pizza:
            return None

        return PizzaDTO(**pizza[0].dict())

    async def find_by_name(self, name: str) -> Optional[PizzaDTO]:
        """Find one pizza by name from read model."""
        pizzas = await PizzaModel.from_queryset(Pizzas.filter(name=name))

        if not pizzas:
            return None

        return PizzaDTO(**pizzas[0].dict())
