from enum import unique
from tortoise import fields
from tortoise.models import Model


class ScrapedPlant(Model):
    id = fields.IntField(pk=True)
    common_names = fields.CharField(200)
    latin_name = fields.CharField(50, unique=True)
    additional = fields.JSONField(null=True)
