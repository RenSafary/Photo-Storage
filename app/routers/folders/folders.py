from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from models.Users import Users
from models.Folders import Folders
from models.Files import Files
from routers.auth.sign_in import AuthService
from routers.gallery.gallery import Gallery
from utils.storage.get_files import get_files

auth = AuthService()

gallery = Gallery()
gallery_router = gallery.router


class FoldersR:
    def __init__(self):
        self.router = APIRouter()
        self.tmpl = Jinja2Templates(directory="./app/templates/folders/")

        self.router.add_api_route("/gallery/folders/", self.all_folders, methods=["GET"])
        self.router.add_api_route("/gallery/folders/{username}/{folder}", self.current_folder, methods=["GET"])
        self.router.include_router(gallery_router, prefix="/api")

    async def all_folders(self, request: Request):
        user = auth.verify_token(request)
        if not user:
            return HTMLResponse(status_code=401, content="<H1>401</H1> <H2>Not authorized</H2>")
        else:
            username = Users.get(Users.username == user)
            folders = Folders.select().where(Folders.user == username)

            return self.tmpl.TemplateResponse(request, "folders.html", {
                "user": username.username,
                "folders": folders
                })
    
    async def current_folder(
        self,
        username: str,
        folder: str,
        request: Request
        ):
        user = auth.verify_token(request)
        if not user:
            return HTMLResponse(status_code=401, content="<H1>401</H1> <H2>Not authorized</H2>")
        else:
            files = get_files(username, folder)

            return self.tmpl.TemplateResponse(request, "folder.html", {"files": files})