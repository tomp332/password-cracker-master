from typing import Annotated

from fastapi import APIRouter, UploadFile, File, HTTPException

from password_cracker_master import master_context
from password_cracker_master.server.models.responses import UploadFileResponse
from password_cracker_master.server.routes.password_routes.utils import load_passwords_from_file

passwords_router = APIRouter(prefix="/api/passwords")


@passwords_router.post("/upload", response_model=UploadFileResponse)
async def create_upload_file(file: Annotated[UploadFile, File(description="Password hashes to be cracked")]):
    try:
        # check the content type (MIME type)
        content_type = file.content_type
        if content_type not in ["text/plain"]:
            raise HTTPException(status_code=400, detail="Invalid file type, only text files allowed")
        contents = file.file.read()
        with open(master_context.main_settings.data_dir_path / file.filename, 'wb') as f:
            f.write(contents)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=400, detail="Bad file uploaded")
    finally:
        file.file.close()
        file_response: UploadFileResponse = UploadFileResponse(file_name=file.filename, file_size=file.size)
        # Store the file data in the database
        await load_passwords_from_file(file_response_model=file_response)
    return file_response
