from typing import List

from uvicorn.main import logger

from password_cracker_master import master_context
from password_cracker_master.server.models.minion_tasks_models import MinionTasksModel, CreateMinionTaskModel


async def get_all_tasks(skip: int, limit: int) -> List[MinionTasksModel]:
    """
    Get all tasks from the database

    :param skip: Skip first N tasks
    :param limit: Limit tasks to N
    :return: List of MinionTasksModel
    """
    logger.debug(f"Getting {skip} to {limit} tasks from the database")
    return await master_context.db_object.tasks_collection.find().skip(skip).limit(limit).to_list(length=limit)


async def add_new_minion_task(task: CreateMinionTaskModel):
    """
    Add new task to the database

    :param task: CreateMinionTaskModel
    """
    logger.debug(f"Adding new task to the database: {task}")
    await master_context.db_object.tasks_collection.insert_one(MinionTasksModel(**task.dict()).dict())
    logger.debug(f"Added new task to the database: {task}")


async def write_current_start_range(start_range: int):
    """
    Write the current start range to the database

    :param start_range: int
    """
    logger.debug(f"Writing current start range to the database: {start_range}")
    await master_context.db_object.tasks_collection.update_one({"_id": "current_start_range"},
                                                               {"$set": {"start_range": start_range}})
