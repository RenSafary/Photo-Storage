from fastapi import APIRouter, Request, Form, UploadFile, File
from datetime import datetime
from typing import List
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from peewee import *

from models.Users import Users
from models.Folders import Folders
from models.Files import Files

from routers.auth.sign_in import AuthService
from routers.gallery.gallery import Gallery

from utils.storage.get_files import get_files
from utils.storage.upload_files import upload_files

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
        self.router.include_router(gallery_router, prefix="/api")
        self.router.add_api_route("/gallery/folders/creation", self.create_folder, methods=["POST"])
        self.router.add_api_route("/gallery/folders/{username}/{folder}", self.current_folder, methods=["GET"])
        self.router.add_api_route("/gallery/folders/{username}/{folder}/upload_in_folder", self.add_in_folder, methods=["POST"])
        self.router.add_api_route("/gallery/folders/{username}/{folder}/delete_file/{file_id}", self.delete_file_in_folder, methods=["GET"])
        self.router.add_api_route("/gallery/folders/{username}/{folder}/delete_folder", self.delete_folder, methods=["GET"])

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
            user = Users.get(Users.username == user)
            
            # files in folder
            files_folder = get_files(username, folder)

            # getting folder id
            redis_folder = redis_folders(user)
            for folder_ in redis_folder:
                if folder_['name'] == folder:
                    folder_id = folder_['id']
                    break

            # getting files
            all_files = redis_files(user)

            files_by_folder = list()

            for file in all_files:
                if file['folder_id'] == folder_id:
                    files_by_folder.append(file)

            files_aws = get_files(username, files_by_folder)
            
            all_files_list = list()

            for file_info, file_data in zip(files_by_folder, files_aws):
                file_obj = {
                    'id': file_info.get('id'),
                    'key': file_data.get('key'),
                    'folder_id': file_info.get('folder_id'),
                    'url': file_data.get('url'),
                    'size': file_data.get('size')
                }
                all_files_list.append(file_obj)

            return self.tmpl.TemplateResponse(request, "folder.html",
                {
                    "files_folder": files_folder,
                    "all_files": all_files_list,
                    "user": user.username,
                    "folder": folder
                })
        
    async def add_in_folder(
        self,
        username: str,
        folder: str,
        media_file: List[UploadFile] = File(...),
    ):
        username_db = Users.get(username=username)

        time_today = datetime.today()

        prefix = username + "/"

        for file in media_file:
            if not file:
                print("It is not a file")
            else:
                file_path = f"{username}/{folder}/{file.filename}"
                file_size = round(file.size / (1024*1024)) 

                response = upload_files(prefix, file_path, file, file_size)

                if response.get("status") == "error":
                    return HTMLResponse(content='<H1>Storage is full!</H1><p>Get more space!</p>', status_code=500)
                else:
                    file_path_db = Files.create(
                        user=username_db, 
                        link=file_path, 
                        date_uploaded=time_today,
                        size_of_file_bytes=file_size,
                        )
                    # redis
                    self.refresh_rdb(username)
                    
                    
        return RedirectResponse(f"/gallery/folders/{username}/{folder}/", status_code=303)

    async def delete_file_in_folder(
        self,
        username: str,
        folder: str,
        file_id: str
    ):  
        files = (Files.update(folder_id=None).where(Files.id == file_id).execute())

        self.refresh_rdb(username)

        return RedirectResponse(url=f"/gallery/folders/{username}/{folder}", status_code=302)
        
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
    
    async def delete_folder(
            self,
            request: Request,
            username: str,
            folder: str,
    ):
        user = auth.verify_token(request)
        if user != username:
            return HTMLResponse(content="Forbidden", status=403)
            
        user = Users.get(Users.username == username)
        folders = redis_folders(user)

        for i in folders:
            if folder == i['name']:
                folder = i['id']
                break

        try:
            Files.update(folder_id=None).where(Files.folder_id == folder).execute()
            Folders.delete().where(Folders.id == folder).execute()
        except DatabaseError as DBerr:
            print(DBerr)
        except DoesNotExist:
            print(DoesNotExist)
        return RedirectResponse(url="/gallery/folders", status_code=303)