from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from models.Users import Users
from models.Tags import Tags
from models.Files import Files
from routers.auth.sign_in import AuthService
from utils.storage.get_files import get_files


auth = AuthService()

class Files_By_Tag:
    def __init__(self):
        self.router = APIRouter()
        self.template = Jinja2Templates(directory="./app/templates/tags/")

        self.router.add_api_route("/{tag}/{username}/", self.show_files, methods=["GET"])

    async def show_files(
        self, 
        tag: str,
        username: str,
        request: Request
        ):
        user = auth.verify_token(request)

        if not user or (user != username):
            return RedirectResponse("/sign-in", status_code=401)
        else:
            tag_db = Tags.get_or_none(Tags.name == tag)
            if not tag_db:
                return HTMLResponse(status_code=404, content=f"<H1>Tag {tag} not found</H1>")
            else:
                file_links = Files.select().where(Files.tag == tag)
                file_links = list(file_links)
                files = get_files(username, file_links)
                return self.template.TemplateResponse(request, "files_by_tag.html", {"files": files})