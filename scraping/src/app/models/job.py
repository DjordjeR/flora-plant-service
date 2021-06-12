from enum import Enum
from tortoise import fields
from tortoise.models import Model

class JobTypeEnum(str, Enum):
    done = "done"
    running = "running"
    stopped = "stopped"
    error = "error"

class ScrapeJob(Model):
    id = fields.IntField(pk=True)
    status = fields.CharEnumField(max_length=10, enum_type=JobTypeEnum)
    plant_name = fields.CharField(50)
    result = fields.JSONField()