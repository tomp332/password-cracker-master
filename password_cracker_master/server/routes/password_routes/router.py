from fastapi import APIRouter, UploadFile, HTTPException, BackgroundTasks
from starlette.requests import Request

from password_cracker_master.schemas.responses import UploadFileResponse
from password_cracker_master.server.routes.password_routes.utils import load_passwords_from_file, generate_hash, \
    upload_file_grid

passwords_router = APIRouter(prefix="/api/passwords")


@passwords_router.post('/upload', response_model=UploadFileResponse, summary="Upload a file_obj with password hashes")
async def upload(request: Request, file: UploadFile, background_tasks: BackgroundTasks):
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
