from typing import List

from uvicorn.main import logger

from password_cracker_master import master_context
from password_cracker_master.schemas.enums import StatusEnum
from password_cracker_master.src.models.minions_models import CreateMinionModel, MinionsModel, UpdateMinionModel, \
    MinionSignUpsModel


async def add_minion(new_minion: CreateMinionModel) -> dict:
    """
    Add a new minion to the database
    """
    logger.debug(f"Adding new minion to the database, {new_minion.minion_hostname}:{new_minion.minion_id}")
    return await master_context.db_object.minions_collection.insert_one(MinionsModel(**new_minion.dict()).dict())


async def get_all_online_minions(limit: int = 10) -> List[dict]:
    """
    Get all tasks from the database

    :return: List of MinionsModel
    """
    logger.debug(f"Getting all online minions from the database")
    return await master_context.db_object.minions_collection.find({"status": StatusEnum.ONLINE}).to_list(length=limit)


async def update_minion_information(minion_id: str, updated_data: UpdateMinionModel) -> dict:
    """
    Add a new minion to the database

    :param updated_data: Data to update
    :param minion_id: Minion ID to update
    :return: Updated result
    """
    logger.debug(f"Updating minion status in the database, {minion_id}:{updated_data.dict()}")
    return await master_context.db_object.minions_collection.update_one({"minion_id": minion_id},
                                                                        {'$set': updated_data.dict()})


async def get_minion_signups(limit: int, find_filter: dict = None, sort_filter: dict = None, skip: int = 0) -> List[
    MinionSignUpsModel]:
    """
    Get all tasks from the database

    :param skip: Skip first N tasks
    :param limit: Limit tasks to N
    :param sort_filter: Filter sorting tasks
    :return: List of MinionSignUpsModel
    """
    logger.debug(f"Getting {skip} to {limit} minion tasks from the database")
    return await master_context.db_object.minion_signup_collection.find(not find_filter and {}).sort(
        not sort_filter and {}).skip(skip).limit(
        limit).to_list(length=limit)
