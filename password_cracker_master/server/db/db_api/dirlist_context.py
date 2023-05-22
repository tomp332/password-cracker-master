from typing import Optional

from pymongo.collection import Collection
from uvicorn.main import logger

from password_cracker_master import master_context
from password_cracker_master.server.models.dirlist_models import DirListContextModel


async def get_current_seek() -> tuple[Optional[int], Optional[str]]:
    """
    Get current seek from database
    """
    logger.debug("Fetching current dirlist seek from database")
    current_seek: dir = await master_context.db_object.dirlist_context_collection.find_one() or {}
    logger.info(f"Current dirlist seek: {current_seek.get('current_seek')}")
    return current_seek.get("seek_pointer"), current_seek.get("_id") and f'{current_seek.get("_id")}' or None


async def update_current_seek(collection_obj: Collection, current_seek: int):
    """
    Add current seek to database
    """


async def add_current_seek(current_seek: int) -> str:
    """
    Add current seek to database
    """
    logger.info("Adding current dirlist seek to database")
    a = await master_context.db_object.dirlist_context_collection.insert_one(
        DirListContextModel(seek_pointer=current_seek).dict())
    return f'{a.inserted_id}'
