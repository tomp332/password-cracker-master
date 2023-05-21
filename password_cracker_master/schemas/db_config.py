from pydantic import BaseModel


class MongoConnectionSchema(BaseModel):
    """
    Schema for Mongo Connection
    """
    username: str
    password: str
    host: str
    port: int
