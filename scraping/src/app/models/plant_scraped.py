from enum import unique
from tortoise import fields
from tortoise.models import Model


class ScrapedPlant(Model):
    id = fields.IntField(pk=True)
    common_names = fields.CharField(200, null=True)
    latin_name = fields.CharField(100, unique=True)
    additional = fields.JSONField(null=True)
