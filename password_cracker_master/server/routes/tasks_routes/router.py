from typing import List

from fastapi import APIRouter

from password_cracker_master.server.db.db_api.tasks import get_all_tasks
from password_cracker_master.server.models.minion_tasks_models import MinionTasksModel

tasks_router = APIRouter(prefix="/api/tasks")


@tasks_router.get("/", summary="Get all password cracking tasks")
async def get_tasks(skip: int = 0, limit: int = 20) -> List[MinionTasksModel]:
    return await get_all_tasks(skip=skip, limit=limit)
