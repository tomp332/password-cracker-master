from typing import List, Optional

from fastapi import APIRouter, Response
from starlette import status
from uvicorn.main import logger

from password_cracker_master import master_context
from password_cracker_master.schemas.responses import MinionSignUpResponse
from password_cracker_master.server.models.minion_tasks_models import StatusEnum
from password_cracker_master.server.routes.minion_routes.utils import fetch_dirlist_range

minion_router = APIRouter(prefix="/api/minion")


@minion_router.get("/signup", response_model=MinionSignUpResponse,
                   summary="Minion signup for new password range",
                   responses={204: {"model": None}})
async def minion_signup(limit: int, minion_id: str, minion_hostname: str, response: Response):
    logger.debug(f"Received minion signup request, {minion_hostname}:{minion_id}")
    # Fetch the current hashed password to be cracked
    password_obj: Optional[dict] = await master_context.db_object.passwords_collection.find_one(
        {"status": StatusEnum.PENDING})
    # {).to_list(1)
    if not password_obj:
        # No password to crack
        response.status_code = status.HTTP_204_NO_CONTENT
        response.description = "No password to crack"
        return MinionSignUpResponse()
    else:
        # Fetch range of dictionary passwords to try
        hash_range: List[str] = await fetch_dirlist_range(skip=master_context.current_dirlist_cursor_index,
                                                          limit=limit)
        # Update the current hashed password to be cracked
        await master_context.set_current_dirlist_cursor_index(
            new_value=master_context.current_dirlist_cursor_index + len(hash_range))
        logger.info(f"Minion signup successful, minion_id: {minion_id}, range_size: {len(hash_range)}")
        return MinionSignUpResponse(crack_task_id=password_obj.get("crack_task_id"), crack_hash_range=hash_range,
                                    password=password_obj.get("password_hash"))


@minion_router.post("/cracked", summary="Minion submit cracked password")
async def minion_cracked_password():
    # Need to implement
    # Need to start a new brute force
    master_context.set_current_dirlist_cursor_index(new_value=0)
    pass
