from dataclasses import asdict, dataclass

from result import Err, Ok, Result

from pizzeria.system.bus import Command, Handler
from pizzeria.system.domain.errors import DomainError

from ...domain.errors import DuplicatedNameError, DuplicatedPizzaIdError
from ...domain.model import Pizza, PizzaFactory, PizzaId
from ...domain.repository import PizzaRepository
from ..services import PizzaFinder


@dataclass
class AddPizzaCommand(Command):
    """Add pizza command."""

    id: str
    name: str
    price: int
    toppings: list[str]


class AddPizzaCommandHandler(Handler[AddPizzaCommand, None]):
    """Add pizza command handler."""

    def __init__(
        self,
        repository: PizzaRepository,
        finder: PizzaFinder,
    ) -> None:
        self.__repository = repository
        self.__finder = finder

    async def handle(self, message: AddPizzaCommand) -> Result[None, list[DomainError]]:
        """Handle the message."""
        errors: list[DomainError] = []
        result = PizzaFactory.build(**asdict(message))
        pizza: Pizza

        match result:
            case Ok(pizza):  # type: ignore
                pass
            case Err(_) as err:  # type: ignore
                return err

        if not await self.__check_pizza_id_unique(pizza.id):
            errors.append(DuplicatedPizzaIdError(message.id))

        if not await self.__check_name_unique(message.name):
            errors.append(DuplicatedNameError(message.name))

        if errors:
            return Err(errors)

        await self.__repository.save(pizza)

        return Ok()

    async def __check_pizza_id_unique(self, pizza_id: PizzaId) -> bool:
        exists_pizza_with_this_id = (await self.__repository.get(pizza_id)).unwrap_or(False)

        return exists_pizza_with_this_id is False

    async def __check_name_unique(self, name: str) -> bool:
        found_pizza_with_that_name = await self.__finder.find_by_name(name)

        return found_pizza_with_that_name is None
