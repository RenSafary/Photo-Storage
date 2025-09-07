from fastapi import APIRouter, Request, UploadFile, File, Form
from typing import List
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime
from fastapi.templating import Jinja2Templates
from fastapi.websockets import WebSocket, WebSocketDisconnect
from jose import jwt
from dotenv import load_dotenv
import os
import json
from peewee import *
from boto3 import exceptions

from routers.auth.sign_in import AuthService

from models.Users import Users
from models.Folders import Folders
from models.Files import Files

from utils.storage.size import get_size
from utils.storage.get_files import get_files
from utils.storage.upload_files import upload_files
from utils.storage.delete_file import delete_s3_file

from redis_client.models.files import redis_files
from redis_client.models.user import record_user_in_rdb
from redis_client.connection import connect

auth_service = AuthService()

class Gallery:
    def __init__(self):
        self.router = APIRouter()
        self.tmpl = Jinja2Templates(directory="./app/templates/gallery")

        self.router.add_api_route("/gallery", self.gallery, methods=["GET"])
        self.router.add_api_route("/gallery/upload/", self.upload_files_to_storage, methods=["POST"])
        self.router.add_api_route("/delete/", self.delete_file, methods=["POST"])

        self.router.add_api_websocket_route("/new-folder/ws", self.new_folder)

    def get_current_user(self, token: str):
        load_dotenv()

        SECRET_KEY = os.getenv("SECRET_KEY")
        ALGORITHM = os.getenv("ALGORITHM")

        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username = payload.get("sub")

        return username

    def refresh_rdb(self, user: str):
        user = Users.get(Users.username == user)

        rdb = connect()
        rdb.delete(f"user_id:{user.id}")
        record_user_in_rdb(user)
        print(f"user_id:{user.id} was refreshed")

    async def gallery(self, request: Request):
        try:
            username = auth_service.verify_token(request)
            if not username:
                return RedirectResponse("/sign-in")
            else:
                user = Users.get(Users.username == username)
                
                files = redis_files(user)

                # getting size of all files
                prefix = username + "/"
                total_size, total_files = get_size(prefix)

                files = get_files(username, files)

                return self.tmpl.TemplateResponse(
                    "gallery.html", {
                        "request": request, 
                        "user": user,
                        "username": username, 
                        "size" : total_size,
                        "files": files
                        })
        except Exception as e:
            print(f"Problem in gallery: {e}")
            return RedirectResponse('/Photo-Storage')

    async def new_folder(self, websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                try:
                    data = await websocket.receive_json()
                    new_folder = data["new_folder"]
                    token = data["access_token"]
                    username = self.get_current_user(token[13::])
                    user = Users.get(Users.username == username)

                    if Folders.get_or_none(
                        (Folders.user == user) & (Folders.name == new_folder)
                    ):
                        await websocket.send_json(
                            {"status": "error", "detail": "Folder name is already taken"}
                        )
                    else:
                        folder = Folders.create(name=new_folder, user=user.id)

                        # redis
                        self.refresh_rdb(username)
                        
                        await websocket.send_json({"status": "success", "token": token})
                        
                except WebSocketDisconnect:
                    break
                    
                except json.JSONDecodeError:
                    await websocket.send_json(
                        {"status": "error", "detail": "Invalid JSON format"}
                    )
                    
                except Exception as e:
                    print("Error in gallery.py websocket:", e)
                    await websocket.send_json(
                        {"status": "error", "detail": str(e)}
                    )
                    await websocket.close(code=1008)
                    break
                    
        except Exception as e:
            print("Unexpected error:", e)
        finally:
            try:
                await websocket.close()
            except RuntimeError:
                pass 

    async def upload_files_to_storage(
        self,
        user: str = Form(...),
        media_file: List[UploadFile] = File(...),
    ):
        username_db = Users.get(username=user)

        time_today = datetime.today()

        prefix = user + "/"

        for file in media_file:
            if not file:
                print("It is not a file")
            else:
                file_path = f"{user}/{file.filename}"
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
                    self.refresh_rdb(user)
                    
                    
        return RedirectResponse(f"/gallery/", status_code=303)

    async def delete_file(
        self,
        file_path: str = Form(...)
    ):
        try:
            # getting username
            splited_path = file_path.split("/")
            username = splited_path[0]

            file = Files.get(Files.link == file_path)

            file.delete_instance()

            response = delete_s3_file(file_path)
            if response.status_code == 200:
                # redis
                self.refresh_rdb(username)

                return RedirectResponse("/gallery", status_code=200) 
            else:
                return HTMLResponse(f"<H1>{response.status_code}</H1><p>{response.content}</p>")
        except exceptions as s3_exceptions:
            print("Exception before deleting file from bucket:", s3_exceptions)