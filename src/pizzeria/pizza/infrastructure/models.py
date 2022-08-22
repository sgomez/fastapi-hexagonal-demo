from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Pizzas(models.Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=90, unique=True)
    price = fields.IntField()
    toppings = fields.JSONField()


PizzaModel = pydantic_model_creator(Pizzas, name="Pizza")
