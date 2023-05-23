from typing import List

from uvicorn.main import logger

from password_cracker_master import master_context
from password_cracker_master.schemas.responses import CrackTaskPasswordsResponse
from password_cracker_master.src.models.passwords_models import PasswordModel, UpdatePasswordModel


async def retrieve_passwords_by_crack_task_id(crack_task_id: str, limit: int = 50) -> List[CrackTaskPasswordsResponse]:
    """
    Retrieve all passwords

    :param crack_task_id: The crack task id
    :param limit: The length of the list to return
    :return: List of PasswordModel
    """
    a = await master_context.db_object.passwords_collection.find({"crack_task_id": crack_task_id}).to_list(
        length=limit)
    logger.debug(f"Retrieved passwords from the database, {a}")
    return [CrackTaskPasswordsResponse(**x) for x in a]


async def add_password_hash(password_hash: str, crack_task_id: str) -> List[PasswordModel]:
    """
    Retrieve all passwords

    :param password_hash: The hashed password to add
    :param crack_task_id: The crack task id
    :return: List of PasswordModel
    """
    # Load password to DB
    return await master_context.db_object.passwords_collection.insert_one(
        PasswordModel(password_hash=password_hash, crack_task_id=crack_task_id).dict())


async def update_password_information(password_hash: str, updated_data: UpdatePasswordModel) -> dict:
    """
    Add a new minion to the database

    :param updated_data: Data to update
    :param password_hash: The hashed password to update information for
    :return: Updated result
    """
    logger.debug(f"Updating password information in the database, {password_hash}:{updated_data.dict()}")
    return await master_context.db_object.passwords_collection.update_one({"password_hash": password_hash},
                                                                          {'$set': updated_data.dict()})
