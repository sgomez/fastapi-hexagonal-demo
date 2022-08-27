from typing import Any, Optional

import strawberry
from strawberry.types import Info

from pizzeria.system.strawberry.errors import DomainErrorContext, ValidationError
from pizzeria.system.strawberry.types import Context, from_global_id

from ....application.commands.add_pizza import AddPizzaCommand
from ....domain import errors as domain_errors
from ..types import PizzaInput, PizzaNode


@strawberry.type
class NameAlreadyExistsError(ValidationError):
    ...


AddPizzaError = strawberry.union(
    "AddPizzaError",
    (NameAlreadyExistsError, ValidationError),
)


@strawberry.type
class AddPizzaResponse:
    pizza: Optional[PizzaNode]
    errors: list[AddPizzaError]


class AddPizzaDomainErrorContext(DomainErrorContext):
    def __exit__(self, exc_type, exc_value, traceback):

        self.success = False

        match exc_value:
            case domain_errors.DuplicatedNameError(_) as err:
                self.errors.append(
                    NameAlreadyExistsError(
                        message=err.message,
                        code=err.code,
                        path=err.label,
                    )
                )
            case _:
                return super().__exit__(exc_type, exc_value, traceback)

        return True


async def add_pizza_resolver(input: PizzaInput, info: Info[Context, Any]) -> AddPizzaResponse:
    with AddPizzaDomainErrorContext() as context:
        await info.context.command_bus.dispatch(
            AddPizzaCommand(
                id=from_global_id(input.id),
                name=input.name,
                price=input.price,
                toppings=input.toppings,
            )
        )

    if not context.success:
        return AddPizzaResponse(pizza=None, errors=context.errors)

    return AddPizzaResponse(pizza=PizzaNode.build_from_input(input), errors=[])
