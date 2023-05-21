import re
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field, validator


class PasswordSchema(BaseModel):
    """
    PasswordSchema is the model for the password to be cracked
    """
    # id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    password_hash: str = Field(...)
    password_plaintext: str = ""
    password_cracked: bool = Field(default=False)
    password_cracked_by: str = Field(default=None)
    crack_task_id: str

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
    password_hash: Optional[str]
    password_plaintext: Optional[str]
    password_cracked: Optional[bool]
    password_cracked_by: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
