import pathlib

from pydantic import BaseSettings, Field, validator


class MasterBaseSettings(BaseSettings):
    """
    Master server base settings
    """
    # Framework Settings
    framework_hostname: str = Field(default='0.0.0.0', env='FRAMEWORK_HOSTNAME')
    framework_port: int = Field(default=8000, env='FRAMEWORK_PORT')

    # Data
    data_dir_path: pathlib.Path = Field(default='/data', env='DATA_DIR_PATH')

    @validator('data_dir_path', pre=True, always=True)
    def validate_data_dir_path(cls, value):
        pathlib.Path(value).mkdir(parents=True, exist_ok=True)
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


class MainMasterSettings(DbSettings, MasterBaseSettings):
    """
    Main settings for master server
    """
    pass