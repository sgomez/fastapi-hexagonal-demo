from typing import Any, Callable, Optional
from uuid import UUID

from result import Result
from strawberry import ID
from strawberry.types import Info

from pizzeria.system.domain.errors import DomainError
from pizzeria.system.strawberry.types import Context, from_global_id

from ....application.queries.get_pizza import GetPizzaQuery, GetPizzaQueryResult
from ..types import PizzaNode


async def pizza_resolver(info: Info[Context, Any], id: ID) -> Optional[PizzaNode]:
    """Get a pizza."""
    id_ = UUID(from_global_id(id))

    query_result: Result[GetPizzaQueryResult, list[DomainError]] = await info.context.query_bus.dispatch(
        GetPizzaQuery(id_)
    )

    to_pizza_node: Callable[[GetPizzaQueryResult], PizzaNode] = lambda x: PizzaNode.build_from_response(
        x.pizza
    )

    return query_result.map_or(None, to_pizza_node)
