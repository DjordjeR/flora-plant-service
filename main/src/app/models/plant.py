from enum import unique
from tortoise import fields
from tortoise.models import Model


class Plant(Model):
    id = fields.IntField(pk=True)
    common_name = fields.CharField(50, unique=True)
    latin_name = fields.CharField(50, unique=True)
    metadata = fields.JSONField(null=True)
