"""
Singleton class to store global variables
"""
from typing import Optional

from uvicorn.main import logger

from password_cracker_master.schemas.config import MainMasterSettings
from password_cracker_master.server.db.db_config import MongoConnectionSchema
from password_cracker_master.server.db.main_db import FrameworkDB


class MainContext:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """

        """
        self.main_settings: MainMasterSettings = MainMasterSettings()
        self._current_dirlist_cursor_index: int = 0
        self.current_dirlist_cursor_id: Optional[str] = None
        self.db_object: FrameworkDB = FrameworkDB(
            MongoConnectionSchema(username=self.main_settings.db_user,
                                  password=self.main_settings.db_password,
                                  host=self.main_settings.db_host,
                                  port=self.main_settings.db_port)
        )

    @property
    def current_dirlist_cursor_index(self):
        return self._current_dirlist_cursor_index

    async def set_current_dirlist_cursor_index(self, new_value: int):
        logger.info(f"Updating current dirlist seek to database, value by: {new_value}")
        await self.db_object.dirlist_context_collection.update_one({}, {'$set': {"seek_pointer": new_value}},
                                                                   upsert=True)
        self._current_dirlist_cursor_index = new_value
