from typing import Any

from strawberry.types import Info

from pizzeria.system.strawberry.types import Context

from ....application.queries.get_pizzas import GetPizzasQuery, GetPizzasQueryResult
from ..types import PizzaNode


async def pizzas_resolver(info: Info[Context, Any]) -> list[PizzaNode]:
    response: GetPizzasQueryResult = await info.context.query_bus.dispatch(GetPizzasQuery())

    return [PizzaNode.build_from_response(pizza) for pizza in response.pizzas]
