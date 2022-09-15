import strawberry

from .mutations.add_pizza import add_pizza_resolver
from .queries.get_pizza import pizza_resolver
from .queries.get_pizzas import pizzas_resolver


@strawberry.type
class Mutation:
    """Pizza mutations."""

    add_pizza = strawberry.mutation(resolver=add_pizza_resolver)


@strawberry.type
class Query:
    """Pizza queries."""

    pizza = strawberry.field(resolver=pizza_resolver)
    pizzas = strawberry.field(resolver=pizzas_resolver)
