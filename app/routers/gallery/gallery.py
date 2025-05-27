from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.exceptions import HTTPException
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

from routers.auth.sign_in import AuthService
from utils.storage.size import get_size
from models.Users import Users
from models.Folders import Folders
from models.Tags import Tags
from models.Files import Files
from utils.storage.get_files import get_files
from utils.storage.upload_files import upload_files
from utils.storage.delete_file import delete_s3_file

auth_service = AuthService()

class Gallery:
    def __init__(self):
        self.router = APIRouter()
        self.tmpl = Jinja2Templates(directory="./app/templates/gallery")

        self.router.add_api_route("/gallery", self.gallery, methods=["GET"])
        self.router.add_api_route("/gallery/upload/", self.upload_files_to_storage, methods=["POST"])
        self.router.add_api_route("/delete/", self.delete_file, methods=["POST"])

        self.router.add_api_websocket_route("/new-folder/ws", self.new_folder)
        self.router.add_api_websocket_route("/new-tag/ws", self.new_tag_ws)

    def get_current_user(self, token: str):
        load_dotenv()

        SECRET_KEY = os.getenv("SECRET_KEY")
        ALGORITHM = os.getenv("ALGORITHM")

        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username = payload.get("sub")

        return username

    async def gallery(self, request: Request):
        try:
            username = auth_service.verify_token(request)
            if not username:
                return RedirectResponse("/sign-in")
            else:
                user = Users.get(Users.username == username)
                folders = Folders.select().where(Folders.user == user.id)

                # getting size of all files
                prefix = username + "/"
                total_size, total_files = get_size(prefix)

                file_links = Files.select().where(Files.user == user)
                file_links = list(file_links)
                files = get_files(username, file_links)

                return self.tmpl.TemplateResponse(
                    "gallery.html", {
                        "request": request, 
                        "user": user, 
                        "folders": folders, 
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

    async def new_tag_ws(self, websocket: WebSocket):
        await websocket.accept()
        try:
            data = await websocket.receive_json()
            name = data["name"]
            token = data["access_token"]
            username = self.get_current_user(token[13::])
            user = Users.get(Users.username == username)
            if not user:
                await websocket.send_json(
                    {'status':'error', 'detail':'Not authorized'}
                )
            else:
                tag = Tags.get_or_none(Tags.name == name, Tags.user == user)
                if not tag:
                    tag = Tags.create(name=name, user=user)
                await websocket.send_json(
                    {'status':'success', 'token': token}
                )


        except WebSocketDisconnect:
            print("Connection is closed")
        except DatabaseError as e:  
            print("Database error in gallery.new_tag", e)
        except Exception as e:
            print("Error in gallery.new_tag:", e)
        finally:
            try:
                await websocket.close()
            except:
                pass

    async def upload_files_to_storage(
        self,
        user: str = Form(...),
        tag: str = Form(...),
        media_file: List[UploadFile] = File(...),
    ):
        username_db = Users.get(username=user)

        time_today = datetime.today()

        prefix = user + "/"

        print(f"user: {username_db.username}, tag: {tag}")
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
                        tag=tag
                        )
        return RedirectResponse(f"/gallery/", status_code=303)

    async def delete_file(
        self,
        file_path: str = Form(...)
    ):
        file = Files.get(Files.link == file_path)

        file.delete_instance()

        response = delete_s3_file(file_path)
        if response.status_code == 200:
            return RedirectResponse("/gallery", status_code=200) 
        else:
            return HTMLResponse(f"<H1>{response.status_code}</H1><p>{response.content}</p>")