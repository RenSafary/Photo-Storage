from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from database import get_ch_client
from models.user import UserCreate, User

router = APIRouter()

tmpl = Jinja2Templates(directory="./app/templates/")


@router.get("/sign-up")
async def sign_up(request: Request):
    return tmpl.TemplateResponse("sign_up.html", {"request": request})


@router.post("/sign-up/proccess")
async def sign_up_proccess(
    username: str = Form(...), password: str = Form(...), email: str = Form(...)
):

    return JSONResponse({"username": username, "password": password, "email": email})
