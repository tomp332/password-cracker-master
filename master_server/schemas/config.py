from pydantic import BaseSettings, Field


class MasterBaseSettings(BaseSettings):
    """
    Master server base settings
    """
    # Framework Settings
    framework_hostname: str = Field(default='0.0.0.0', env='FRAMEWORK_HOSTNAME')
    framework_port: int = Field(default=8000, env='FRAMEWORK_PORT')

    # DB Settings
    db_host: str = Field(default='cracker-db', env='DB_HOST')
    db_port: int = Field(default=27017, env='DB_PORT')
    db_user: str = Field(default='admin', env='DB_USER')
    db_password: str = Field(default='admin', env='DB_PASSWORD')
