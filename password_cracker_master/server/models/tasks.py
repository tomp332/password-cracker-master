from enum import Enum
from typing import List

from bson import ObjectId
from pydantic import BaseModel, Field


class StatusEnum(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class TasksModel(BaseModel):
    """
    TasksModel is the model for the tasks representing a password cracking task
    """
    crack_task_id: str = Field(...)
    minion_server_attacked: List[str] = Field(...)
    password_hash: str = Field(...)
    status: StatusEnum = Field(default=StatusEnum.PENDING)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
