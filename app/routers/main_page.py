from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from routers.auth.sign_in import verify_token

router = APIRouter()

tmpl = Jinja2Templates(directory="./app/templates")

@router.get("/")
async def main_page(request: Request):
    username = verify_token(request)
    return tmpl.TemplateResponse("main.html",
    {
        'request': request,
        'username': username
    })

@router.get("/log-out")
async def log_out(
    response: Response
):
    response = RedirectResponse("/sign-in")
    response.delete_cookie(
        key="access_token",
        path="/",
        secure=True,
        httponly=True,
        samesite="lax"
    )
    return response