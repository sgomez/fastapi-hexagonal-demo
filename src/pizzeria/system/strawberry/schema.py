import strawberry
from fastapi import Depends
from strawberry.fastapi import GraphQLRouter
from strawberry.tools import merge_types

from pizzeria.pizza.infrastructure import graphql as pizza_schema

from ..container import Container, build_container
from .types import Context

__queries = merge_types(
    "Queries",
    (pizza_schema.Query,),
)


__mutations = merge_types(
    "Mutations",
    (pizza_schema.Mutation,),
)


schema = strawberry.Schema(query=__queries, mutation=__mutations)


async def __get_context(
    container: Container = Depends(build_container),
) -> Context:
    return Context(
        query_bus=container.query_bus,
        command_bus=container.command_bus,
    )


graphql_router = GraphQLRouter(schema, context_getter=__get_context)
