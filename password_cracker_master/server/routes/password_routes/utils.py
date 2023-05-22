import binascii
import os

from pydantic import ValidationError
from uvicorn.main import logger

from password_cracker_master import master_context
from password_cracker_master.server.db.db_api.passwords import add_password_hash
from password_cracker_master.server.db.db_api.tasks import add_new_minion_task
from password_cracker_master.schemas.errors import FrameworkError, FrameworkErrorCodesEnum
from password_cracker_master.server.models.minion_tasks_models import MinionTasksModel


def read_fs_file(file_hash: str) -> str:
    """
    read_fs_file reads the file from the database

    :param file_hash: The file hash
    :return: Yields a file data row
    """


async def load_passwords_from_file(file_hash: str, crack_task_id: str):
    """
    Load passwords from file_obj to the database

    :param file_hash: The file hash
    :param crack_task_id: The crack task id
    """
    try:
        logger.info(f"Loading password from file_hash: {file_hash}, crack_task_id: {crack_task_id}")
        # Paginate file content from GridFS in database
        hashes_cursor = master_context.db_object.fs.find({"filename": file_hash}, no_cursor_timeout=True)
        while await hashes_cursor.fetch_next:
            hashes_grid_out = hashes_cursor.next_object()
            hashes_data = await hashes_grid_out.read()
            for password_hash in hashes_data.decode().splitlines():
                await add_password_hash(password_hash=password_hash, crack_task_id=crack_task_id)
                # Create a task for the current password hash for future cracking
                await add_new_minion_task(task=MinionTasksModel(crack_task_id=crack_task_id,
                                                                password_hash=password_hash))
                logger.debug(f"Added password hash to DB: {password_hash}")
    except ValidationError as e:
        logger.error(f"Error while loading passwords from file_obj: {e}")
        raise FrameworkError(message=f'{e}',
                             status_code=FrameworkErrorCodesEnum.PASSWORD_FORMAT_ERROR)


async def generate_hash():
    return binascii.hexlify(os.urandom(16)).decode()


async def upload_file_grid(file_obj: object, file_name: str, file_hash: str, extra_metadata: dict = None,
                           read_needed: bool = True):
    """
    Uploads a file to the database using GridFS

    :param file_obj: The file to upload
    :param file_hash: The file hash
    :param file_name: The file name
    :param extra_metadata: Extra metadata to add to the file
    :param read_needed: Whether to read the file or not
    """
    try:
        logger.debug(f"Uploading file to database, {file_name}:{file_hash}")
        extra_metadata = extra_metadata or {}
        grid_in = master_context.db_object.fs.open_upload_stream(
            file_hash, metadata={'contentType': "text/plain", 'filename': file_name, **extra_metadata})
        if read_needed:
            data = await file_obj.read()
        else:
            data = file_obj
        await grid_in.write(data)
        await grid_in.close()
        logger.info(f"Finished uploading file successfully to database, {file_name}:{file_hash}")
    except Exception as e:
        raise FrameworkError(f"Error uploading file_obj to database: {e}",
                             status_code=FrameworkErrorCodesEnum.DIRLIST_FILE_ERROR)
