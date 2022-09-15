from typing import Any, Callable

from result import Result
from strawberry.types import Info

from pizzeria.system.domain.errors import DomainError
from pizzeria.system.strawberry.types import Context

from ....application.queries.get_pizzas import GetPizzasQuery, GetPizzasQueryResult
from ..types import PizzaNode


async def pizzas_resolver(info: Info[Context, Any]) -> list[PizzaNode]:
    """Get all pizzas."""
    query_result: Result[GetPizzasQueryResult, list[DomainError]] = await info.context.query_bus.dispatch(
        GetPizzasQuery()
    )

    to_pizza_node_list: Callable[[GetPizzasQueryResult], list[PizzaNode]] = lambda x: [
        PizzaNode.build_from_response(pizza) for pizza in x.pizzas
    ]

    return query_result.map_or([], to_pizza_node_list)
