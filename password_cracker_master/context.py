"""
Singleton class to store global variables
"""

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
        self.current_dirlist_cursor_index: int = 0
        self.db_object: FrameworkDB = FrameworkDB(
            MongoConnectionSchema(username=self.main_settings.db_user,
                                  password=self.main_settings.db_password,
                                  host=self.main_settings.db_host,
                                  port=self.main_settings.db_port)
        )
