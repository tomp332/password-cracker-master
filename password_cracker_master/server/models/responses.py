import uuid

from pydantic import BaseModel, Field


class UploadFileResponse(BaseModel):
    """
    UploadFileResponse is the model for the response of the file upload
    """
    file_name: str
    file_size: int
    crack_task_id: str = Field(default=f'{uuid.uuid4()}', description="The ID of the crack task")
