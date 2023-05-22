import asyncio
from typing import List, Optional

from uvicorn.main import logger

from password_cracker_master import master_context
from password_cracker_master.server.db.db_api.minion_signups import get_minion_signups
from password_cracker_master.server.models.minion_signup import MinionSignUpsModel
from password_cracker_master.server.models.minion_tasks import StatusEnum
from password_cracker_master.server.routes.password_routes.utils import upload_file_grid, generate_hash


async def validate_minion_signups():
    """
    validate_minion_signups validates the minion signups in the database
    """
    minion_requests_to_be_handled: List[MinionSignUpsModel] = await get_minion_signups(limit=20,
                                                                                       find_filter={
                                                                                           "state": StatusEnum.ACCEPTED},
                                                                                       sort_filter={"timestamp": -1})
    while minion_requests_to_be_handled:
        for minion_request in minion_requests_to_be_handled:
            pass


async def startup_actions():
    """
    startup_actions is a function that is called on startup of the server
    """
    await load_dirlist_file()


async def load_dirlist_file():
    # Check if the dirlist has been loaded to database before already
    dirlist_file: Optional[dict] = await master_context.db_object.fs.find({
        "metadata.filename": master_context.main_settings.dirlist_path.name}).limit(1).to_list(1)
    # Check if the dirlist has been loaded to database before already
    if not dirlist_file or dirlist_file[-1].get("length") != master_context.main_settings.dirlist_path.stat().st_size or \
            master_context.main_settings.dirlist_load_force:
        # Load the dirlist to the database in a background task
        logger.info("Loading dirlist to database for the first time, this may take a while...")
        file_data, file_hash = await load_large_file()
        asyncio.create_task(upload_file_grid(file_obj=file_data, file_hash=file_hash,
                                             file_name=master_context.main_settings.dirlist_path.name,
                                             read_needed=False))


async def load_large_file():
    """
    Loads the dirlist file to memory and generates a hash for it

    :return: file_data, file_hash
    """
    file_obj = open(master_context.main_settings.dirlist_path, "rb")
    file_data = file_obj.read()
    file_hash = await generate_hash()
    file_obj.close()
    return file_data, file_hash
