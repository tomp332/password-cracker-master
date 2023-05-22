import asyncio
from typing import Optional

from uvicorn.main import logger

from password_cracker_master import master_context
from password_cracker_master.server.db.db_api.dirlist_context import get_current_seek, add_current_seek
from password_cracker_master.server.routes.password_routes.utils import upload_file_grid, generate_hash


async def startup_actions():
    """
    startup_actions is a function that is called on startup of the server
    """
    await load_dirlist_file()
    # Handle dirlist seek pointer
    current_seek, seek_id = await get_current_seek()
    if not seek_id:
        master_context.current_dirlist_cursor_id = await add_current_seek(
            current_seek=master_context.current_dirlist_cursor_index)
    else:
        # Need to restore the seek pointer and seek ID from the database
        master_context.current_dirlist_cursor_id = seek_id
        await master_context.set_current_dirlist_cursor_index(new_value=current_seek)


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
