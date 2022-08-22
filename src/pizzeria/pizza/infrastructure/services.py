from typing import List, Optional

from ..application.queries import PizzaFinder, PizzaQueryResult
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


class TortoisePizzaFinder(PizzaFinder):
    async def find_all(self) -> List[PizzaQueryResult]:
        pizzas = await PizzaModel.from_queryset(Pizzas.all())

        return [PizzaQueryResult(**pizza.dict()) for pizza in pizzas]

    async def find_by_name(self, name: model.PizzaName) -> Optional[PizzaQueryResult]:
        pizzas = await PizzaModel.from_queryset(Pizzas.filter(name=name.value))

        if not pizzas:
            return None

        return PizzaQueryResult(**pizzas[0].dict())
