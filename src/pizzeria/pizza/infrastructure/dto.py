from dataclasses import asdict
from typing import List
from uuid import UUID

from pydantic import BaseModel

from ..application.queries import PizzaQueryResult

# region requests


class AddPizzaRequest(BaseModel):
    name: str
    price: int
    toppings: List[str]


# endregion


# region responses


class PizzaResponse(BaseModel):
    id: UUID
    name: str
    price: int
    toppings: List[str]

    @staticmethod
    def fromPizzaQueryResponse(obj: PizzaQueryResult) -> "PizzaResponse":
        return PizzaResponse.parse_obj(asdict(obj))


class PizzasResponse(BaseModel):
    pizzas: list[PizzaResponse]


# endregion
