from typing import Any, Optional

import strawberry
from result import Err, Result
from strawberry.types import Info

from pizzeria.system.domain.errors import DomainError
from pizzeria.system.strawberry.errors import ValidationError
from pizzeria.system.strawberry.types import Context, from_global_id

from ....application.commands.add_pizza import AddPizzaCommand
from ....domain import errors as domain_errors
from ..types import PizzaInput, PizzaNode


@strawberry.type
class NameAlreadyExistsError(ValidationError):
    """Pizza name already exists error."""


@strawberry.type
class PizzaIdAlreadyExistsError(ValidationError):
    """Pizza id already exists error."""


AddPizzaError = strawberry.union(
    "AddPizzaError",
    (PizzaIdAlreadyExistsError, NameAlreadyExistsError, ValidationError),
)


@strawberry.type
class AddPizzaResponse:
    """Add pizza mutation response."""

    pizza: Optional[PizzaNode]
    errors: list[AddPizzaError]


def domain_errors_to_graphql_errors_mapper(errors: list[DomainError]) -> list[AddPizzaError]:
    """Map errors between domain errors and mutation errors."""
    mapped_errors: list[AddPizzaError] = []
    for error in errors:
        match error:
            case domain_errors.DuplicatedPizzaIdError(_) as err:
                mapped_errors.append(
                    PizzaIdAlreadyExistsError(
                        message=err.message,
                        code=err.code,
                        path=err.label,
                    )
                )
            case domain_errors.DuplicatedNameError(_) as err:
                mapped_errors.append(
                    NameAlreadyExistsError(
                        message=err.message,
                        code=err.code,
                        path=err.label,
                    )
                )
            case domain_errors.ValidationError(_) as err:
                mapped_errors.append(
                    ValidationError(
                        message=err.message,
                        code=err.code,
                        path=err.label,
                    )
                )

    return mapped_errors


async def add_pizza_resolver(input: PizzaInput, info: Info[Context, Any]) -> AddPizzaResponse:
    """Add a pizza."""
    mutation_result: Result[None, list[DomainError]] = await info.context.command_bus.dispatch(
        AddPizzaCommand(
            id=from_global_id(input.id),
            name=input.name,
            price=input.price,
            toppings=input.toppings,
        )
    )

    errors: list[AddPizzaError] = []
    pizza: Optional[PizzaNode] = None

    match mutation_result:
        case Err(errors):  # type: ignore
            pass
        case _:
            pizza = PizzaNode.build_from_input(input)

    return AddPizzaResponse(pizza=pizza, errors=errors)
