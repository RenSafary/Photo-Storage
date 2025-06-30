from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from routers.auth.sign_in import AuthService
from models.Users import Users
from redis_client.connection import connect

router = APIRouter()

tmpl = Jinja2Templates(directory="./app/templates")

auth_service = AuthService()


@router.get("/Photo-Storage")
async def main_page(request: Request):
    username = auth_service.verify_token(request)
    if not username:
        return RedirectResponse("/sign-in")
    else:
        return tmpl.TemplateResponse(
            "main.html", {"request": request, "username": username}
        )

@router.get("/log-out")
async def log_out(request: Request, response: Response):
    try:
        user = auth_service.verify_token(request)
        print(user)
        user = Users.get_or_none(Users.username == user)
         
        redis_cli = connect()

        redis_cli.delete(f"user_id:{user.id}")

        if not user:
            return RedirectResponse("/Photo-Storage")
        else:
            response = RedirectResponse("/Photo-Storage")
            response.delete_cookie(
                key="access_token", path="/", secure=True, httponly=True, samesite="lax"
            )
            return response
    except Exception as e:
        print(f"Error in main_page.py: {e}")
        return RedirectResponse("/Photo-Storage")
