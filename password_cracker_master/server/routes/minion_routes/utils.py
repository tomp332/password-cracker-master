from typing import List

from gridfs import GridOut
from requests import post, Response
from uvicorn.main import logger

from password_cracker_master import master_context
from password_cracker_master.schemas.enums import StatusEnum
from password_cracker_master.server.db.db_api.files import fetch_file_info
from password_cracker_master.server.db.db_api.minions import get_all_online_minions, update_minion_information
from password_cracker_master.server.db.db_api.passwords import update_password_information
from password_cracker_master.server.models.minions_models import MinionFinishedTaskModel, MinionsModel, \
    UpdateMinionModel
from password_cracker_master.server.models.passwords_models import UpdatePasswordModel


async def fetch_dirlist_range(skip: int = 0, limit: int = 2) -> List[str]:
    """
    Fetches a range of dictionary passwords to try

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
    start_position: int = master_context.main_settings.dirlist_password_length * skip
    grid_out.seek(start_position)
    while data := await grid_out.read(master_context.main_settings.dirlist_password_length) and len(
            password_hashes) != limit:
        password_hashes.extend(data.decode().splitlines())
    logger.debug(
        f"Fetched dirlist range for minion signup, skip: {skip}, limit: {limit}, total_size: {len(password_hashes)}")
    # Return the list of dictionary passwords to try
    return password_hashes


async def handle_finished_crack_logic(finished_task_model: MinionFinishedTaskModel):
    """
    Handles the logic for when a minion finishes cracking a password
    """
    # Need to start a new brute force reset the dirlist seek
    master_context.set_current_dirlist_cursor_index(new_value=0)
    # Update the proper information based on the finished task
    await update_password_information(password_hash=finished_task_model.hashed_password,
                                      updated_data=UpdatePasswordModel(**finished_task_model.dict()))
    # Stop all minions
    # TODO: Implement this


async def notify_all_minions():
    """
    Notifies all minions that there is a new password to crack
    """
    # Iterate over all online minions and send them a notification to stop working
    while online_minions := await get_all_online_minions(limit=20):
        for minion in online_minions:
            current_minion: MinionsModel = MinionsModel(**minion)
            # Send the minion a notification to stop working
            response: Response = post(
                url=f"http://{current_minion.minion_hostname}:{master_context.main_settings.minions_rest_port}/api/kill")
            if response.status_code != 200:
                logger.error(
                    f"Failed to notify minion {current_minion.minion_hostname} to stop working, response: {response.json()}")
            else:
                logger.info(f"Successfully notified minion {current_minion.minion_hostname} to stop working")
                # Update minion status to offline
                await update_minion_information(minion_id=current_minion.minion_id,
                                                updated_data=UpdateMinionModel(status=StatusEnum.OFFLINE))
