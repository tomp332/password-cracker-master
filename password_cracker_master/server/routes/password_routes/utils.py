from uvicorn.main import logger

from password_cracker_master import master_context
from password_cracker_master.server.db.db_api.passwords import add_password_hash
from password_cracker_master.server.models.responses import UploadFileResponse


def large_file_reader(file_name) -> str:
    """
    Read a large file line by line
    """
    for password in open(file_name, "r"):
        yield password


async def load_passwords_from_file(file_response_model: UploadFileResponse):
    """
    Load passwords from file to the database

    :param file_response_model: UploadFileResponse model
    """
    for password_hash in large_file_reader(master_context.main_settings.data_dir_path / file_response_model.file_name):
        logger.debug(f"Loaded password from file: {password_hash}")
        # Load password to DB
        await add_password_hash(password_hash=password_hash, crack_task_id=file_response_model.crack_task_id)
