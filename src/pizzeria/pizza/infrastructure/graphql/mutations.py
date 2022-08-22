from typing import Any, Optional

import strawberry
from strawberry.types import Info

from pizzeria.system.domain.exception import DomainErrorContext
from pizzeria.system.strawberry.types import Context, Node, UserError, from_global_id

from ...application.commands import AddPizzaCommand
from .types import PizzaInput, PizzaNode


@strawberry.type
class NameAlreadyExistsError(UserError):
    ...


AddPizzaError = strawberry.union(
    "AddPizzaError",
    (NameAlreadyExistsError,),
)


@strawberry.type
class AddPizzaPayload:
    pizza: Optional[PizzaNode]
    errors: list[AddPizzaError]


async def add_pizza_resolver(input: PizzaInput, info: Info[Context, Any]) -> AddPizzaPayload:
    with DomainErrorContext() as context:
        await info.context.command_bus.dispatch(
            AddPizzaCommand(
                id=from_global_id(input.id),
                name=input.name,
                price=input.price,
                toppings=input.toppings,
            )
        )

    if not context.success:
        return AddPizzaPayload(pizza=None, errors=[NameAlreadyExistsError(message=input.name, path="name")])

    return AddPizzaPayload(pizza=PizzaNode.build_from_input(input), errors=[])


@strawberry.type
class Mutation:
    add_pizza = strawberry.mutation(resolver=add_pizza_resolver)
