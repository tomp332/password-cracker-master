from typing import List

import requests.exceptions
from gridfs import GridOut
from requests import post, Response
from uvicorn.main import logger

from password_cracker_master import master_context
from password_cracker_master.schemas.enums import StatusEnum
from password_cracker_master.schemas.responses import MinionNewTaskResponse
from password_cracker_master.src.db.db_api.files import fetch_file_info
from password_cracker_master.src.db.db_api.minions import get_all_online_minions, update_minion_information
from password_cracker_master.src.db.db_api.passwords import update_password_information
from password_cracker_master.src.db.db_api.tasks import add_new_minion_task
from password_cracker_master.src.models.minions_models import MinionFinishedTaskModel, MinionsModel, \
    NotifyMinionModel, UpdateMinionModel, CreateMinionTaskModel
from password_cracker_master.src.models.passwords_models import UpdatePasswordModel


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
    while (data := await grid_out.read(master_context.main_settings.dirlist_password_length)) and len(
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
    await notify_all_minions()


async def notify_all_minions():
    """
    Notifies all minions that there is a new password to crack
    """
    # Iterate over all online minions and send them a notification to stop working
    while online_minions := await get_all_online_minions(limit=20):
        for minion in online_minions:
            current_minion: MinionsModel = MinionsModel(**minion)
            try:
                # Send the minion a notification to stop working
                response: Response = post(
                    url=f"http://{current_minion.minion_hostname}:{master_context.main_settings.minions_rest_port}/api/kill",
                    json=NotifyMinionModel(password_hash=current_minion.current_password_hash).json())
                if response.status_code != 200:
                    logger.error(
                        f"Failed to notify minion {current_minion.minion_hostname} to stop working, response: {response.json()}")
                else:
                    logger.info(f"Successfully notified minion {current_minion.minion_hostname} to stop working")
            except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
                logger.error(f"Failed to notify all minions, error: {e}")
                # Update minion status to offline
                await update_minion_information(minion_id=current_minion.minion_id,
                                                updated_data=UpdateMinionModel(status=StatusEnum.OFFLINE))


async def handle_new_minion_task(minion_id: str, limit: int, password_hash: str) -> MinionNewTaskResponse:
    """
    Handles the logic for when a new minion signs up

    :param minion_id: The id of the minion
    :param limit: The number of dictionary passwords to try
    :param password_hash: The password hash to crack
    :return: The new minion task response model
    """
    # Fetch range of dictionary passwords to try
    hash_range: List[str] = await fetch_dirlist_range(skip=master_context.current_dirlist_cursor_index,
                                                      limit=limit)
    # Update the current hashed password to be cracked
    await master_context.set_current_dirlist_cursor_index(
        new_value=master_context.current_dirlist_cursor_index + len(hash_range))
    new_minion_task: CreateMinionTaskModel = CreateMinionTaskModel(
        password_hash=password_hash,
        minion_id=minion_id,
        hash_range_end=master_context.current_dirlist_cursor_index,
    )
    # Add minion task to DB
    await add_new_minion_task(task=new_minion_task)
    # Return the new minion task
    return MinionNewTaskResponse(task_id=new_minion_task.task_id, crack_hash_range=hash_range,
                                 password=password_hash)
