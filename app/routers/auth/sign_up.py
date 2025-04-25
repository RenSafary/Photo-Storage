from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import bcrypt

from models.users import Users, db

router = APIRouter()

tmpl = Jinja2Templates(directory="./app/templates/")


@router.get("/sign-up")
async def sign_up(request: Request):
    return tmpl.TemplateResponse("auth/sign_up.html", {"request": request})


@router.post("/sign-up/proccess")
async def sign_up_proccess(
    email: str = Form(...), username: str = Form(...), password: str = Form(...)
):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    try:
        db.connect()
        
        user = Users.create(email=email, username=username, password=hashed_password)
    except Exception as e:
        print(f"Error db: {e}")
    finally:
        db.close()
    return RedirectResponse("/")
