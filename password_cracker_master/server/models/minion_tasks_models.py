import datetime
from enum import Enum

from bson import ObjectId
from pydantic import BaseModel, Field


class StatusEnum(str, Enum):
    ACCEPTED = "accepted"
    APPLIED = "applied"
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class CreateMinionTaskModel(BaseModel):
    """
    CreateMinionTaskModelCreateMinionTaskModel is the model for the task that is sent to the minion server
    """
    password_hash: str = Field(...)
    hash_range_chunk_id: str = Field(default="123")
    minion_server_hostname: str = Field(default="minion-localhost")
    minion_server_id: str = Field(default="123")
    crack_task_id: str = Field(...)


class MinionTasksModel(CreateMinionTaskModel):
    """
    MinionTasksModel is the model for the tasks representing a password cracking task
    """
    status: StatusEnum = Field(default=StatusEnum.PENDING)
    timestamp: datetime.datetime = datetime.datetime.now()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
