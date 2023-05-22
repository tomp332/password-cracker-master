import uuid
from typing import List

from pydantic import BaseModel, Field


class UploadFileResponse(BaseModel):
    """
    UploadFileResponse is the model for the response of the file_obj upload
    """
    message: str = Field(default="File uploaded processing")
    file_name: str
    file_size: int
    crack_task_id: str = Field(default=f'{uuid.uuid4()}', description="The ID of the crack task")


class MinionSignUpResponse(BaseModel):
    """
    MinionSignUpResponse is the model for the response from the minion server
    """
    password: str = Field(default="")
    crack_hash_range: List[str] = []
    crack_task_id: str = ""
