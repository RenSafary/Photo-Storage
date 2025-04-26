from fastapi import APIRouter, Request, Form, Cookie, Depends   
from fastapi.templating import Jinja2Templates
from jose import jwt

from routers.auth.sign_in import verify_token

router = APIRouter()
tmpl = Jinja2Templates(directory="./app/templates/gallery")

@router.get("/gallery")
async def files(request: Request):
    return tmpl.TemplateResponse('gallery.html',{'request': request})


@router.post("/new-folder")
async def new_folder(
    request: Request,
    new_folder: str = Form(...),
):
    username = verify_token(request)
    print(username)
    return