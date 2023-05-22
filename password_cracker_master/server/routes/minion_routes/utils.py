from typing import List

from gridfs import GridOut
from uvicorn.main import logger

from password_cracker_master import master_context
from password_cracker_master.server.db.db_api.files import fetch_file_info


async def fetch_dirlist_range(skip: int = 0, limit: int = 2) -> List[str]:
    """
    fetch_dirlist_range fetches a range of dictionary passwords to try

    :param skip: The number of dictionary passwords to skip
    :param limit: The number of dictionary passwords to return
    :return: A list of dictionary passwords to try
    """
    # The cursor for the dirlist file from the database
    dirlist_hash, dirlist_file_id = await fetch_file_info(file_name=master_context.main_settings.dirlist_path.name)
    # Open the file_obj from the database
    grid_out: GridOut = await master_context.db_object.fs.open_download_stream(file_id=dirlist_file_id)
    password_hashes: List[str] = []
    # Read and process chunks
    logger.debug(f"Fetching dirlist range for minion signup, skip: {skip}, limit: {limit}")
    start_position: int = 12 * skip
    grid_out.seek(start_position)
    while data := await grid_out.read(12):
        # Read line by line and append to the list
        if not data:
            # No more passwords to brute force, this is a failure
            return []
        if len(password_hashes) == limit:
            break
        password_hashes.extend(data.decode().splitlines())
    logger.debug(
        f"Fetched dirlist range for minion signup, skip: {skip}, limit: {limit}, total_size: {len(password_hashes)}")
    # Return the list of dictionary passwords to try
    return password_hashes
