import motor
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from pymongo.collection import Collection

from password_cracker_master.src.db.db_config import MongoConnectionSchema


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class FrameworkDB:
    """
    Framework database class
    """

    def __init__(self, mongo_config: MongoConnectionSchema):
        self.db_url: str = f"mongodb://{mongo_config.username}:{mongo_config.password}@" \
                           f"{mongo_config.host}:{mongo_config.port}"
        self.client: motor.AsyncIOMotorClient = motor.motor_asyncio.AsyncIOMotorClient(self.db_url)
        self.db = self.client.password_cracker
        self.fs = AsyncIOMotorGridFSBucket(self.db)

        # Collection objects
        self.passwords_collection: Collection = self.db.get_collection("passwords_collection")
        self.tasks_collection: Collection = self.db.get_collection("tasks_collection")
        self.minions_collection: Collection = self.db.get_collection("minions_collection")
        self.dirlist_context_collection: Collection = self.db.get_collection("dirlist_context_collection")

