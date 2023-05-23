import uuid
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class UploadFileResponse(BaseModel):
    """
    UploadFileResponse is the model for the response of the file_obj upload
    """
    message: str = Field(default="File upload processing")
    file_name: str
    file_size: int
    crack_task_id: Optional[str] = Field(description="The ID of the crack task")

    @validator("crack_task_id", pre=True, always=True)
    def crack_task_id_default(cls, v):
        return v or f'{uuid.uuid4()}'


class MinionNewTaskResponse(BaseModel):
    """
    MinionNewTaskResponse is the model for the response from the minion src
    """
    password: str = ""
    task_id: Optional[str]
    crack_hash_range: List[str] = []

    @validator("task_id", pre=True, always=True)
    def generate_uuid(cls, v):
        """
        generate uuid4
        """
        return f'{uuid.uuid4()}'


class MinionSignUpResponse(BaseModel):
    """
    MinionSignUpResponse is the model for the response from the minion src
    """
    minion_id: str


class CrackTaskPasswordsResponse(BaseModel):
    """
    CrackTaskPasswords is the model for the response from the minion src
    """
    password_hash: str
    password_plaintext: str
    status: str
