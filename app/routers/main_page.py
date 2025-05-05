from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from routers.auth.sign_in import verify_token

router = APIRouter()

tmpl = Jinja2Templates(directory="./app/templates")


@router.get("/Photo-Storage")
async def main_page(request: Request):
    username = verify_token(request)
    if not username:
        return RedirectResponse("/sign-in")
    else:
        return tmpl.TemplateResponse(
            "main.html", {"request": request, "username": username}
        )


@router.get("/log-out")
async def log_out(request: Request, response: Response):
    try:
        user = verify_token(request)
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
