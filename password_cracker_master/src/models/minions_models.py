import datetime
import uuid
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from password_cracker_master.schemas.enums import StatusEnum


class CreateMinionModel(BaseModel):
    """
    CreateMinionModel is the model for creating minions
    """
    minion_hostname: str = Field(...)
    minion_id: str = Field(default=f'{uuid.uuid4()}')
    current_password_hash: str = ""
    crack_task_id: str = ""


class MinionsModel(CreateMinionModel):
    """
    MinionsModel is the model for minions
    """

    status: StatusEnum = Field(default=StatusEnum.ONLINE)
    timestamp: datetime.datetime = datetime.datetime.now()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateMinionModel(BaseModel):
    """
    UpdateMinionModel is the model for updating minions
    """
    status: Optional[StatusEnum]
    current_password_hash: Optional[str]
    crack_task_id: Optional[str]


class CreateMinionTaskModel(BaseModel):
    """
    CreateMinionTaskModelCreateMinionTaskModel is the model for the task that is sent to the minion src
    """
    password_hash: str = Field(...)
    minion_id: str = Field(...)
    hash_range_end: int = Field(...)
    task_id: str = Field(default=f'{uuid.uuid4()}')


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


class MinionFinishedTaskModel(BaseModel):
    """
    MinionFinishedTaskModel is the model for the task that is sent to the minion src
    """
    hashed_password: str = Field(...)
    password_plaintext: str = Field(...)
    crack_task_id: str = Field(...)


class NotifyMinionModel(BaseModel):
    """
    NotifyMinionModel is the model for the notification that is sent to the minion src
    """
    password_hash: str = Field(...)
