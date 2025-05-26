from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from models.Users import Users
from models.Tags import Tags
from models.Files import Files
from models.Folders import Folders


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
        
        return