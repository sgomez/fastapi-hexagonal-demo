from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class PizzaDTO:
    id: UUID
    name: str
    price: int
    toppings: list[str]
