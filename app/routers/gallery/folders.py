from fastapi import APIRouter, Request, UploadFile, File, Form, HTTPException
from fastapi.exceptions import HTTPException
from typing import List
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime

from routers.auth.sign_in import AuthService
from models.Users import Users
from models.Folders import Folders
from models.Files import Files
from models.Tags import Tags
from utils.storage.get_files import get_files
from utils.storage.upload_files import upload_files
from utils.storage.delete_file import delete_s3_file
from utils.storage.size import get_size

auth_service = AuthService()

class FoldersR:
    def __init__(self):
        self.router = APIRouter()
        self.tmpl = Jinja2Templates(directory="./app/templates/gallery/")
        
        self.router.add_api_route("/folder/{username}/{folder_name}", self.in_folder, methods=["GET"])
        self.router.add_api_route("/folder/{username}/{folder_name}/uploading/", self.upload_files_to_storage, methods=["POST"])
        self.router.add_api_route("/delete/", self.delete_file, methods=["POST"])

    async def in_folder(
        self,
        username: str, 
        folder_name: str, 
        request: Request
    ):
        try:
            current_user = auth_service.verify_token(request)
            
            if username != current_user:
                return HTMLResponse(
                    content="<h1>403 Forbidden</h1><p>You don't have access to this folder</p>",
                    status_code=403
                )
            
            user = Users.get(Users.username == current_user)
            folder = Folders.get_or_none(
                (Folders.user == user.id) & 
                (Folders.name == folder_name)
            )

            tags = Tags.select().where(Tags.user == user.id)

            if not folder:
                return HTMLResponse(
                    content=f"<h1>404 Not Found</h1><p>Folder '{folder_name}' doesn't exist</p>",
                    status_code=404
                )
            
            files = get_files(user.username, folder.name)
            
            return self.tmpl.TemplateResponse(
                "folders.html",
                {
                    "request": request,
                    "user": current_user,
                    "folder_name": folder_name,
                    "folder": folder,
                    "files": files,
                    "tags": tags
                }
            )
            
        except HTTPException:
            raise
            
        except Exception as e:
            print(f"Error in folder view: {str(e)}")
            return HTMLResponse(
                content=f"<h1>500 Server Error</h1><p>{str(e)}</p>",
                status_code=500
            )

    async def upload_files_to_storage(
        self,
        username: str,
        folder_name: str,
        tag: str = Form(...),
        media_file: List[UploadFile] = File(...),
    ):
        username_db = Users.get(username=username)
        folder_db = Folders.get(user=username_db.id, name=folder_name)

        time_today = datetime.today()

        prefix = username + "/"

        for file in media_file:
            if not file:
                print("It is not a file")
            else:
                file_path = f"{username}/{folder_name}/{file.filename}"
                file_size = round(file.size / (1024*1024)) 
                response = upload_files(prefix, file_path, file, file_size)

                if response.get("status") == "error":
                    return HTMLResponse(content='<H1>Storage is full!</H1><p>Get more space!</p>', status_code=500)
                else:
                    file_path_db = Files.create(
                        folder=folder_db.id, 
                        link=file_path, 
                        date_uploaded=time_today,
                        size_of_file_bytes=file_size,
                        tag=tag
                        )
        return RedirectResponse(f"/folder/{username}/{folder_name}/", status_code=303)

    async def delete_file(
        self,
        file_path: str = Form(...)
    ):
        response = delete_s3_file(file_path)
        if response.status_code == 200:
            return RedirectResponse("/gallery") # doesn't work
        else:
            return HTMLResponse(f"<H1>{response.status_code}</H1><p>{response.content}</p>")