from typing import Any

import strawberry
from strawberry.types import Info

from pizzeria.system.strawberry.types import Context

from ...application.queries import GetPizzasQuery, PizzasQueryResult
from .types import PizzaNode


async def pizzas_resolver(info: Info[Context, Any]) -> list[PizzaNode]:
    response: PizzasQueryResult = await info.context.query_bus.dispatch(GetPizzasQuery())

    return [PizzaNode.build_from_response(pizza) for pizza in response.pizzas]


@strawberry.type
class Query:
    pizzas = strawberry.field(resolver=pizzas_resolver)
