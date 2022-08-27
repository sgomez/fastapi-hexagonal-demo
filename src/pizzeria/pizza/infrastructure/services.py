from typing import List, Optional
from uuid import UUID

from ..application.dto import PizzaDTO
from ..application.services import PizzaFinder
from ..domain import model
from ..domain.repository import PizzaRepository
from .models import PizzaModel, Pizzas


class TortoisePizzaRepository(PizzaRepository):
    async def save(self, pizza: model.Pizza) -> None:
        await Pizzas(
            id=pizza.id.value,
            name=pizza.name.value,
            price=pizza.price.value,
            toppings=pizza.toppings.values,
        ).save()

    async def get(self) -> None:
        return await super().get()


class TortoisePizzaFinder(PizzaFinder):
    async def find_all(self) -> List[PizzaDTO]:
        pizzas = await PizzaModel.from_queryset(Pizzas.all())

        return [PizzaDTO(**pizza.dict()) for pizza in pizzas]

    async def find(self, id: UUID) -> Optional[PizzaDTO]:
        pizza = await PizzaModel.from_queryset(Pizzas.filter(id=id))

        if not pizza:
            return None

        return PizzaDTO(**pizza[0].dict())

    async def find_by_name(self, name: str) -> Optional[PizzaDTO]:
        pizzas = await PizzaModel.from_queryset(Pizzas.filter(name=name))

        if not pizzas:
            return None

        return PizzaDTO(**pizzas[0].dict())
