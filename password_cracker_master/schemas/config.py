import pathlib

from pydantic import BaseSettings, Field, validator


class MasterBaseSettings(BaseSettings):
    """
    Master src base settings
    """
    # Framework Settings
    framework_hostname: str = Field(default='localhost', env='FRAMEWORK_HOSTNAME')
    framework_port: int = Field(default=5001, env='FRAMEWORK_PORT')
    dirlist_path: pathlib.Path = Field(default=pathlib.Path('/data/dictionary.txt'), env='DIRLIST_PATH')
    dirlist_load_chunk_size: int = Field(default=80000, env='DIRLIST_LOAD_CHUNK_SIZE')
    dirlist_load_force: bool = Field(default=False, env='DIRLIST_LOAD_FORCE')
    dirlist_password_length: int = Field(default=12, env='DIRLIST_PASSWORD_LENGTH')

    # Data
    data_dir_path: pathlib.Path = Field(default='/data', env='DATA_DIR_PATH')

    @validator('data_dir_path', pre=True, always=True)
    def validate_data_dir_path(cls, value):
        """
        Validate the data directory path
        """
        pathlib.Path(value).mkdir(parents=True, exist_ok=True)
        return pathlib.Path(value)

    @validator('dirlist_path', pre=True, always=True)
    def validate_dirlist_path(cls, value):
        """
        Validate the dirlist path
        """
        if not pathlib.Path(value).exists():
            raise ValueError(f"Dirlist file does not exist at {value}")
        return pathlib.Path(value)


class DbSettings(BaseSettings):
    """
    Database settings for framework
    """
    # DB Settings
    db_host: str = Field(default='cracker-db', env='DB_HOST')
    db_port: int = Field(default=27017, env='DB_PORT')
    db_user: str = Field(default='root', env='DB_USER')
    db_password: str = Field(default='root', env='DB_PASSWORD')


class MinionSettings(BaseSettings):
    """
    Minion settings for framework
    """
    # Minion Settings
    minions_rest_port: int = Field(default=5000, env='MINIONS_REST_PORT')


class MainMasterSettings(DbSettings, MasterBaseSettings, MinionSettings):
    """
    Main settings for master src
    """
    pass
