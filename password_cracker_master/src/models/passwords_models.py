import datetime
import re
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field, validator

from password_cracker_master.schemas.enums import StatusEnum


class PasswordModel(BaseModel):
    """
    PasswordModel is the model for the password to be cracked
    """
    password_hash: str = Field(...)
    password_plaintext: str = ""
    password_cracked: bool = Field(default=False)
    status: StatusEnum = Field(default=StatusEnum.PENDING)
    password_cracked_by: str = Field(default=None)
    crack_task_id: str
    timestamp: datetime.datetime = datetime.datetime.now()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    @validator("password_hash", pre=True, always=True)
    def validate_password_hash(cls, value):
        # Validate md5 hash format
        if not re.match(r"^[a-f0-9]{32}$", value):
            raise ValueError("Invalid md5 hash format")
        return value


class UpdatePasswordModel(BaseModel):
    """
    UpdatePasswordModel is the model for updating the password
    """
    password_plaintext: Optional[str]
    password_cracked: Optional[bool]
    password_cracked_by: Optional[str]
    status: Optional[StatusEnum]
