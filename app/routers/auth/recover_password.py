from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
import bcrypt
import secrets
import string
from datetime import datetime, timedelta, timezone

from utils.auth.send_recover_message import send_message
from models.users import Users


router = APIRouter()

tmpl = Jinja2Templates(directory="./app/templates")


def recover_token():
    alphabet = string.ascii_letters + string.digits  # A-Za-z0-9
    return "".join(secrets.choice(alphabet) for _ in range(32))


@router.get("/recover-password")
async def recover_password_page(request: Request):
    return tmpl.TemplateResponse("auth/recover_password_get_link.html", {"request": request})


@router.post("/recover-password/proccess")
async def get_email_and_send_link(email: str = Form(...)):
    try:
        user = Users.get(email=email)
        if not user:
            return HTMLResponse(status_code=404, content="Wrong email")
        
        token = recover_token()
        # Сохраняем только токен, а не полный URL
        user.recover_link = token
        token_expires = datetime.now(timezone.utc) + timedelta(minutes=10)
        user.recover_link_expires = token_expires
        user.save()
        
        # Формируем полный URL только для отправки в письме
        link = f"http://127.0.0.1:8000/recover-password/token={token}"
        send_message(user.email, link)
        
        return RedirectResponse("/", status_code=303)
    except Exception as e:
        return HTMLResponse(status_code=404, content="User doesn't exist")


@router.get("/recover-password/token={token}")
async def verify_token(request: Request, token: str):
    try:
        user = Users.get(recover_link=token)
        if not user:
            return HTMLResponse("Link was expired or doesn't exist", status_code=400)

        time_now = datetime.now(timezone.utc)
        # Ensure recover_link_expires is a datetime object
        if isinstance(user.recover_link_expires, str):
            user.recover_link_expires = datetime.fromisoformat(user.recover_link_expires)
            
        if time_now > user.recover_link_expires:
            user.recover_link = None
            user.recover_link_expires = None
            user.save()
            return HTMLResponse("Link has expired", status_code=400)

        return tmpl.TemplateResponse(
            "auth/recover_password.html", 
            {"request": request, "token": token}
        )
    except Exception as e:
        print(f"Error in recovering password {e}")
        return HTMLResponse("Link was expired or doesn't exist", status_code=400)


@router.post("/recover-password/token={token}/proccess")
async def recover_password_proccess(
    token: str,
    password: str = Form(...),
):
    try:
        user = Users.get(recover_link=token)
        if not user:
            return HTMLResponse("Invalid token", status_code=400)

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        user.password = hashed_password
        user.recover_link = None
        user.recover_link_expires = None
        user.save()

        return RedirectResponse("/sign-in", status_code=303)
    except Exception as e:
        print(f"Error during recovering: {e}")
        print("3")
        return HTMLResponse("Error occurred during password recovery", status_code=500)