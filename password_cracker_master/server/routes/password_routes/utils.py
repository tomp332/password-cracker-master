from pydantic import ValidationError
from uvicorn.main import logger

from password_cracker_master import master_context
from password_cracker_master.server.db.db_api.passwords import add_password_hash
from password_cracker_master.server.db.db_api.tasks import add_new_task
from password_cracker_master.server.models.errors import FrameworkError, FrameworkErrorCodesEnum
from password_cracker_master.server.models.responses import UploadFileResponse
from password_cracker_master.server.models.tasks import TasksModel


def large_file_reader(file_name) -> str:
    """
    Read a large file line by line
    """
    logger.debug(f"Reading file: {file_name}, size: {file_name.stat().st_size}")
    for password in open(file_name, "r"):
        yield f'{password}'.strip().replace('\n', '').replace('\r', '')


async def load_passwords_from_file(file_response_model: UploadFileResponse):
    """
    Load passwords from file to the database

    :param file_response_model: UploadFileResponse model
    """
    try:
        for password_hash in large_file_reader(
                master_context.main_settings.data_dir_path / file_response_model.file_name):
            logger.debug(f"Loaded password from file: {password_hash}")
            # Load password to DB
            await add_password_hash(password_hash=password_hash, crack_task_id=file_response_model.crack_task_id)
            # Create a task for the current password hash for future cracking
            await add_new_task(task=TasksModel(crack_task_id=file_response_model.crack_task_id,
                                               minion_server_attacked=[],
                                               password_hash=password_hash))
            logger.info(f"Added password hash to DB: {password_hash}")
    except ValidationError as e:
        logger.error(f"Error while loading passwords from file: {e}")
        raise FrameworkError(message=f'{e}',
                             status_code=FrameworkErrorCodesEnum.PASSWORD_FORMAT_ERROR)
