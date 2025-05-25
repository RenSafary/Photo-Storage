from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
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

auth_service = AuthService()

class Gallery:
    def __init__(self):
        self.router = APIRouter()
        self.tmpl = Jinja2Templates(directory="./app/templates/gallery")

        self.router.add_api_route("/gallery", self.gallery, methods=["GET"])
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

                return self.tmpl.TemplateResponse(
                    "gallery.html", {"request": request, "user": user, "folders": folders, 'size' : total_size}
                )
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