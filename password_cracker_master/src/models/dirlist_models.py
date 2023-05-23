import datetime

from pydantic import BaseModel, Field


class DirListContextModel(BaseModel):
    """
    DirListContextModel is the model for the context of the directory list
    """
    timestamp: datetime.datetime = datetime.datetime.now()
    seek_pointer: int = Field(...)
