from dataclasses import asdict, dataclass

from pizzeria.system.bus import Command, Handler

from ...domain import errors, model
from ...domain.repository import PizzaRepository
from ..services import PizzaFinder


@dataclass
class AddPizzaCommand(Command):
    id: str
    name: str
    price: int
    toppings: list[str]


class AddPizzaCommandHandler(Handler[AddPizzaCommand, None]):
    def __init__(
        self,
        repository: PizzaRepository,
        finder: PizzaFinder,
    ) -> None:
        self.__repository = repository
        self.__finder = finder

    async def handle(self, message: AddPizzaCommand) -> None:
        pizza = model.PizzaFactory.build(**asdict(message))

        await self.__check_name_unique(message.name)

        await self.__repository.save(pizza)

    async def __check_name_unique(self, name: str) -> None:
        pizza = await self.__finder.find_by_name(name)

        if pizza:
            raise errors.DuplicatedNameError(name)
