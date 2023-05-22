import datetime

from bson import ObjectId
from pydantic import Field, BaseModel

from password_cracker_master.server.models.minion_tasks_models import StatusEnum


class MinionSignUpsModel(BaseModel):
    """
    MinionSignUpsModel is the model for minion signups
    """
    limit: int = Field(...)
    minion_id: str = Field(...)
    timestamp: datetime.datetime = datetime.datetime.now()
    state: StatusEnum = Field(default=StatusEnum.ACCEPTED)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
