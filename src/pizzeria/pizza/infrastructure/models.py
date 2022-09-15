from tortoise import fields, models
from tortoise.contrib.pydantic.creator import pydantic_model_creator

from ..domain.model import PizzaName


class Pizzas(models.Model):
    """Pizzas model."""

    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=PizzaName.NAME_MAX_LENGTH, unique=True)
    price = fields.IntField()
    toppings = fields.JSONField()


PizzaModel = pydantic_model_creator(Pizzas, name="Pizza")
