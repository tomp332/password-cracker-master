from typing import List

from fastapi import APIRouter, UploadFile, HTTPException, BackgroundTasks
from uvicorn.main import logger

from password_cracker_master.schemas.responses import UploadFileResponse, CrackTaskPasswordsResponse
from password_cracker_master.src.db.db_api.passwords import retrieve_passwords_by_crack_task_id
from password_cracker_master.src.routes.password_routes.utils import load_passwords_from_file, generate_hash, \
    upload_file_grid

passwords_router = APIRouter(prefix="/api/passwords")


@passwords_router.get('/status', response_model=List[CrackTaskPasswordsResponse],
                      summary="Get the status of the password cracking task", )
async def status(crack_task_id: str, limit: int = 50):
    try:
        logger.debug(f"Fetching crack task status, ID: {crack_task_id}")
        return await retrieve_passwords_by_crack_task_id(limit=limit, crack_task_id=crack_task_id)
    except Exception as error:
        raise HTTPException(status_code=500,
                            detail=f"Failed to fetch crack task status, ID: {crack_task_id}, error: {error}")


@passwords_router.post('/upload', response_model=UploadFileResponse,
                       summary="Upload a file with password hashes to crack",
                       description="Upload a file with seperated lines of password hashes to crack")
async def upload(file: UploadFile, background_tasks: BackgroundTasks):
    # check the content type (text type)
    content_type = file.content_type
    if content_type not in ["text/plain"]:
        raise HTTPException(status_code=400, detail="Invalid file_obj type, only text files allowed")
    file_hash: str = await generate_hash()
    file_response: UploadFileResponse = UploadFileResponse(file_name=file.filename, file_size=file.size)
    background_tasks.add_task(upload_file_grid, file_obj=file, file_name=file.filename, file_hash=file_hash,
                              extra_metadata={"crack_task_id": file_response.crack_task_id})
    background_tasks.add_task(load_passwords_from_file, file_hash=file_hash, crack_task_id=file_response.crack_task_id)
    return file_response
