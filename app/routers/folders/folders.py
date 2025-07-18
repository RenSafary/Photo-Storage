from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from models.Users import Users
from models.Folders import Folders
from models.Files import Files

from routers.auth.sign_in import AuthService
from routers.gallery.gallery import Gallery

from utils.storage.get_files import get_files

from redis_client.connection import connect
from redis_client.models.user import record_user_in_rdb
from redis_client.models.files import redis_files
from redis_client.models.folders import redis_folders


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
        self.router.add_api_route("/gallery/folders/creation", self.create_folder, methods=["POST"])
        self.router.add_api_route("/gallery/folders/{username}/{folder}/delete_file", self.delete_file_in_folder, methods=["POST"])

    def refresh_rdb(self, user: str):
        user = Users.get(Users.username == user)

        rdb = connect()
        rdb.delete(f"user_id:{user.id}")
        record_user_in_rdb(user)
        print(f"user_id:{user.id} was refreshed")

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
            # redis user cache
            user = Users.get(Users.username == user)
            
            # folder id from cache
            folders_cached = redis_folders(user)
            for folders in folders_cached:
                if folder == folders["name"]:
                    folder = folders["id"]
                    break
            
            # files from cache
            files_cached = redis_files(user)

            files = None
            for file in files_cached:
                if (file["folder_id"] == folder) and (file["user_id"] == user.id):
                    # get files from aws
                    files = get_files(username, file["folder_id"])


            return self.tmpl.TemplateResponse(request, "folder.html", {"files": files})
        
    async def delete_file_in_folder(
        self,
        request: Request,
        username: str,
        folder: str,
        file_link: str = Form(...)
    ):
        
        return
        
    async def create_folder(
        self,
        request: Request,
        folder_name: str = Form(...),
    ):
        # getting user obj
        username = auth.verify_token(request)

        user = Users.get(Users.username == username)        

        try:
            # record to db
            if not Folders.select().where(Folders.user == user.id, Folders.name == folder_name):
                folder = Folders.create(name=folder_name, user=user.id)
                folder.save()
                
                # refresh redis cache
                self.refresh_rdb(username)
        except:
            print(Exception)
        return RedirectResponse(url="/gallery/folders", status_code=302)