from typing import Any, Optional
from uuid import UUID

from strawberry import ID
from strawberry.types import Info

from pizzeria.system.strawberry.types import Context, from_global_id

from ....application.queries.get_pizza import GetPizzaQuery, GetPizzaQueryResult
from ..types import PizzaNode


async def pizza_resolver(info: Info[Context, Any], id: ID) -> Optional[PizzaNode]:
    id_ = UUID(from_global_id(id))

    response: GetPizzaQueryResult = await info.context.query_bus.dispatch(GetPizzaQuery(id_))

    if not response.pizza:
        return None

    return PizzaNode.build_from_response(response.pizza)
