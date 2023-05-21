from typing import List

from uvicorn.main import logger

from password_cracker_master import master_context
from password_cracker_master.server.models.tasks import TasksModel


async def get_all_tasks(skip: int, limit: int) -> List[TasksModel]:
    logger.debug(f"Getting all tasks from the database")
    return await master_context.db_object.tasks_collection.find().skip(skip).limit(limit).to_list(length=limit)


async def add_new_task(task: TasksModel):
    logger.debug(f"Adding new task to the database: {task}")
    await master_context.db_object.tasks_collection.insert_one(task.dict())
    logger.debug(f"Added new task to the database: {task}")
