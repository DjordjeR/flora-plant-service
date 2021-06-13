from tortoise import fields
from tortoise.models import Model


class Plant(Model):
    id = fields.IntField(pk=True)
    latin_name = fields.CharField(256, unique=True)
    common_name = fields.JSONField(default=list())
    metadata = fields.JSONField(default=dict())


class PlantJob(Model):
    id = fields.IntField(pk=True)
    search_query = fields.CharField(256, unique=True)
    job_id = fields.IntField()
