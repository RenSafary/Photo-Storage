from fastapi import APIRouter, Request, File, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List

from routers.auth.sign_in import verify_token 
from utils.storage.upload_files import upload_files
from models.users import Users, Files

router = APIRouter()

tmpl = Jinja2Templates(directory="./app/templates/gallery")

@router.get("/upload")
async def upload_files_page(request: Request):
    return tmpl.TemplateResponse("upload_files.html", {'request': request})

@router.post("/upload/proccess")
async def get_files(
    request: Request,
    media_file: List[UploadFile] = File(...)
):
    username = verify_token(request)
    username_db = Users.get(username=username)
    
    for file in media_file:
        if not file:
            print("X")
        else:
            file_path = f"{username}/{file.filename}"
            upload_files(file_path, file)
            file_path_db = Files.create(user=username_db.id, link=file_path)
    return RedirectResponse("/")