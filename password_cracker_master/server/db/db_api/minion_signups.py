from typing import List

from uvicorn.main import logger

from password_cracker_master import master_context
from password_cracker_master.server.models.minion_signup import MinionSignUpsModel


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
