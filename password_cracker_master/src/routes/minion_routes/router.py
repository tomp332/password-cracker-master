from typing import Optional, Annotated

from fastapi import APIRouter, Response, BackgroundTasks, Query
from starlette import status
from uvicorn.main import logger

from password_cracker_master import master_context
from password_cracker_master.schemas.enums import StatusEnum
from password_cracker_master.schemas.responses import MinionSignUpResponse, MinionNewTaskResponse
from password_cracker_master.src.db.db_api.files import fetch_file_info
from password_cracker_master.src.db.db_api.minions import add_minion, update_minion_information
from password_cracker_master.src.models.minions_models import CreateMinionModel, UpdateMinionModel, \
    MinionFinishedTaskModel
from password_cracker_master.src.routes.minion_routes.utils import handle_finished_crack_logic, \
    handle_new_minion_task

minion_router = APIRouter(prefix="/api/minion")


@minion_router.get("/task", summary="Fetch new crack task", response_model=MinionNewTaskResponse,
                   responses={204: {"model": None}})
async def minion_fetch_task(limit: Annotated[int, Query(le=500, ge=1)], minion_id: str, response: Response,
                            background_tasks: BackgroundTasks):
    # Fetch the current hashed password to be cracked
    password_obj: Optional[dict] = await master_context.db_object.passwords_collection.find_one(
        {"status": StatusEnum.PENDING})

    dirlist_hash, dirlist_file_id = await fetch_file_info(file_name=master_context.main_settings.dirlist_path.name)
    if not password_obj or not dirlist_file_id:
        # No password to crack or dirlist file was not found in database
        response.status_code = status.HTTP_204_NO_CONTENT
        response.description = "No password to crack"
        return MinionNewTaskResponse()
    else:
        new_task: MinionNewTaskResponse = await handle_new_minion_task(minion_id=minion_id, limit=limit,
                                                                       password_hash=password_obj.get("password_hash"))
        # Update minion status to processing
        background_tasks.add_task(update_minion_information, minion_id=minion_id,
                                  updated_data=UpdateMinionModel(status=StatusEnum.PROCESSING,
                                                                 current_password_hash=password_obj.get(
                                                                     "password_hash"),
                                                                 crack_task_id=password_obj.get("crack_task_id")))
        logger.info(
            f"Minion task fetched successfully, minion_id: {minion_id}, range_size: {len(new_task.crack_hash_range)}")
        return new_task


@minion_router.get("/signup", response_model=MinionSignUpResponse, summary="New minion signup")
async def minion_signup(minion_hostname: str):
    logger.debug(f"Received minion signup request, {minion_hostname}")
    # Check if minion already exists
    minion_obj: Optional[dict] = await master_context.db_object.minions_collection.find_one(
        {"minion_hostname": minion_hostname})
    if minion_obj:
        logger.info(f"Minion already exists, minion_id: {minion_obj.get('minion_id')}")
        return MinionSignUpResponse(minion_id=minion_obj.get("minion_id"))
    # Add minion to the database
    new_minion: CreateMinionModel = CreateMinionModel(minion_hostname=minion_hostname)
    await add_minion(new_minion=new_minion)
    logger.info(f"Minion signup successful, minion_id: {new_minion.minion_id}")
    return MinionSignUpResponse(minion_id=new_minion.minion_id)


@minion_router.post("/finished", summary="Minion submit cracked password")
async def minion_cracked_password(finished_task_model: MinionFinishedTaskModel):
    await handle_finished_crack_logic(finished_task_model=finished_task_model)
