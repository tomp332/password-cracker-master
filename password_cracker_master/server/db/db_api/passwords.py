from typing import List

from password_cracker_master import master_context
from password_cracker_master.server.models.passwords import PasswordSchema


async def retrieve_passwords() -> List[PasswordSchema]:
    """
    Retrieve all passwords

    :return: List of PasswordSchema
    """
    return [p async for p in master_context.db_object.passwords_collection.find()]


async def add_password_hash(password_hash: str, crack_task_id: str) -> List[PasswordSchema]:
    """
    Retrieve all passwords

    :return: List of PasswordSchema
    """
    # Load password to DB
    return await master_context.db_object.passwords_collection.insert_one(
        PasswordSchema(password_hash=password_hash, crack_task_id=crack_task_id).dict())
