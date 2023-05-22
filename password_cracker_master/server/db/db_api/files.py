from typing import List, Optional

from password_cracker_master import master_context


async def fetch_file_info(file_name: str) -> tuple[Optional[str], Optional[str]]:
    """
    fetch_file_info fetches the file hash from the database

    :param file_name: The file name
    :return: The file hash
    """
    file_query = master_context.db_object.fs.find({
        "metadata.filename": file_name}).limit(1)
    # Check if the dirlist has been loaded to database before already
    dirlist_file: List[dict] = await file_query.to_list(length=1)
    if not dirlist_file:
        return None, None
    return dirlist_file[0].get("filename"), dirlist_file[0].get("_id")
