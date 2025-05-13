from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
import bcrypt
import secrets
import string
from datetime import datetime, timedelta, timezone

from utils.auth.send_recover_message import send_message
from models import Users

router = APIRouter()

class RecoverPassword:
    def __init__(self):
        self.router = APIRouter()
        self.tmpl = Jinja2Templates(directory="./app/templates/auth")

        self.router.add_api_route("/recover-password", self.recover_password_page, methods=["GET"])
        self.router.add_api_route("/recover-password/proccess", self.get_email_and_send_link, methods=["POST"])
        self.router.add_api_route("/recover-password/token={token}", self.verify_token, methods=["GET"])
        self.router.add_api_route("/recover-password/token={token}/proccess", self.recover_password_proccess, methods=["POST"])

    def recover_token():
        alphabet = string.ascii_letters + string.digits  # A-Za-z0-9
        return "".join(secrets.choice(alphabet) for _ in range(32))

    async def recover_password_page(self, request: Request):
        return self.tmpl.TemplateResponse("recover_password_get_link.html", {"request": request})

    async def get_email_and_send_link(self, email: str = Form(...)):
        try:
            user = Users.get(email=email)
            if not user:
                return HTMLResponse(status_code=404, content="Wrong email")
            
            token = self.recover_token()
            user.recover_link = token
            token_expires = datetime.now(timezone.utc) + timedelta(minutes=10)
            user.recover_link_expires = token_expires
            user.save()
            
            link = f"http://127.0.0.1:8000/recover-password/token={token}"
            send_message(user.email, link)
            
            return RedirectResponse("/", status_code=303)
        except Exception as e:
            return HTMLResponse(status_code=404, content="User doesn't exist")

    async def verify_token(self, request: Request, token: str):
        try:
            user = Users.get(recover_link=token)
            if not user:
                return HTMLResponse("Link was expired or doesn't exist", status_code=400)

            time_now = datetime.now(timezone.utc)
            
            if isinstance(user.recover_link_expires, str):
                user.recover_link_expires = datetime.fromisoformat(user.recover_link_expires)
                
            if time_now > user.recover_link_expires:
                user.recover_link = None
                user.recover_link_expires = None
                user.save()
                return HTMLResponse("Link has expired", status_code=400)

            return self.tmpl.TemplateResponse(
                "recover_password.html", 
                {"request": request, "token": token}
            )
        except Exception as e:
            print(f"Error in recovering password {e}")
            return HTMLResponse("Link was expired or doesn't exist", status_code=400)

    async def recover_password_proccess(
        self,
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