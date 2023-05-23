from typing import List, Annotated

from fastapi import APIRouter, Query

from password_cracker_master.src.db.db_api.tasks import get_all_tasks
from password_cracker_master.src.models.minions_models import MinionTasksModel

tasks_router = APIRouter(prefix="/api/tasks")


@tasks_router.get("/", summary="Get all password cracking tasks")
async def get_tasks(skip: int, limit: Annotated[int, Query(le=100, ge=1)]) -> List[MinionTasksModel]:
    return await get_all_tasks(skip=skip, limit=limit)
