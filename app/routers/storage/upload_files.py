from fastapi import APIRouter, Request, File, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List


router = APIRouter()

tmpl = Jinja2Templates(directory="./app/templates/storage")

@router.get("/upload")
async def upload_files(request: Request):
    return tmpl.TemplateResponse("upload_files.html", {'request': request})

@router.post("/upload/proccess")
async def get_files(
     media_file: List[UploadFile] = File(...)
):
    # обработка формата файла
    # прикрутить добавление файлов в бакеты
    for file in media_file:
        if not file:
            print("X")
        else:
            print("Y")
    return RedirectResponse("/")