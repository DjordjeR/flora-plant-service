from enum import unique
from tortoise import fields
from tortoise.models import Model

class JobTypeEnum(str, Enum):
    done = "done"
    running = "running"
    stopped = "stopped"
    error = "error"

class Job(Model):
    id = fields.IntField(pk=True)
    status = fields.CharEnumField(JobTypeEnum)
    result = fields.JSONField()