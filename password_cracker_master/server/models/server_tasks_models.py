import datetime

from bson import ObjectId
from pydantic import BaseModel, Field

from password_cracker_master.server.models.minion_tasks_models import StatusEnum


class MinionTasksModel(BaseModel):
    """
    MinionTasksModel is the model for the tasks representing a password cracking task
    """
    timestamp: datetime.datetime = datetime.datetime.now()
    password_hash: str
    crack_task_id: str
    status: StatusEnum = Field(default=StatusEnum.PENDING)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
