# region add_pizza

from dataclasses import dataclass

from pizzeria.system.bus import Command, Handler
from pizzeria.system.domain.exception import DomainError

from ..domain import model, repository
from .queries import PizzaFinder

# region AddPizzaCommand


@dataclass
class AddPizzaCommand(Command):
    id: str
    name: str
    price: int
    toppings: list[str]


class AddPizzaCommandHandler(Handler[AddPizzaCommand, None]):
    def __init__(
        self,
        repository: repository.PizzaRepository,
        finder: PizzaFinder,
    ) -> None:
        self.__repository = repository
        self.__finder = finder

    async def handle(self, message: AddPizzaCommand) -> None:
        _id = model.PizzaId.fromString(message.id)
        name = model.PizzaName(message.name)
        price = model.PizzaPrice(message.price)
        toppings = model.PizzaToppings(message.toppings)

        await self.__check_name_unique(name)

        pizza = model.Pizza(_id, name, price, toppings)

        await self.__repository.save(pizza)

    async def __check_name_unique(self, name: model.PizzaName) -> None:
        pizza = await self.__finder.find_by_name(name)

        if pizza:
            raise DomainError("Duplicated name", "name", "duplicated_name")


# endregion AddPizzaCommand
