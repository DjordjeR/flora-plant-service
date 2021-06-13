from enum import unique
from tortoise import fields
from tortoise.models import Model


class ScrapedPlant(Model):
    id = fields.IntField(pk=True)
    common_names = fields.JSONField(default=list())
    latin_name = fields.CharField(100, unique=True)
    additional = fields.JSONField(default=dict())
