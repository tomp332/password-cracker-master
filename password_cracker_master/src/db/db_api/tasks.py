from typing import List

from uvicorn.main import logger

from password_cracker_master import master_context
from password_cracker_master.src.models.minions_models import CreateMinionTaskModel, MinionTasksModel
from password_cracker_master.src.models.server_tasks_models import UpdateMinionTaskModel


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


async def update_task_information(task_id: str, updated_data: UpdateMinionTaskModel) -> dict:
    """
    Update task information in the database

    :param task_id: Task ID
    :param updated_data: Updated data
    """
    logger.debug(f"Updating minion task information in the database, {task_id}:{updated_data.dict()}")
    return await master_context.db_object.tasks_collection.update_one({"task_id": task_id},
                                                                      {'$set': updated_data.dict()})
