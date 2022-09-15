from dataclasses import dataclass
from typing import TypeAlias
from uuid import UUID


@dataclass(frozen=True)
class PizzaDTO:
    """Represents a pizza from the read model."""

    id: UUID
    name: str
    price: int
    toppings: list[str]


PizzasDTO: TypeAlias = list[PizzaDTO]
