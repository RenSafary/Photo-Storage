from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


from routers.auth.sign_in import verify_token
from models.users import Users, Folders, Files
from utils.storage.get_files import get_files

router = APIRouter()

tmpl = Jinja2Templates(directory="./app/templates/")

@router.get("/folder/{username}/{folder_name}")
async def in_folder(
    username: str,
    folder_name: str,
    request: Request
):
    try:
        user = verify_token(request)
        if username != user:
            return HTMLResponse(content="Not allowed", status_code=403)
        else:
            return HTMLResponse(content="Hello", status_code=200)

        
    except:
        return HTMLResponse(content="You are not logged in", status_code=401)