from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.websockets import WebSocket, WebSocketDisconnect
from jose import jwt
from dotenv import load_dotenv
import os
import json

from routers.auth.sign_in import verify_token
from utils.storage.get_files import get_files
from models import Users, Folders


router = APIRouter()
tmpl = Jinja2Templates(directory="./app/templates/gallery")

def get_current_user(token: str):
    load_dotenv()

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")

    payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
    username = payload.get("sub")

    return username

@router.get("/gallery")
async def gallery(request: Request):
    try:
        username = verify_token(request)
        if not username:
            return RedirectResponse("/sign-in")
        else:
            user = Users.get(Users.username == username)
            folders = Folders.select().where(Folders.user == user.id)
            return tmpl.TemplateResponse(
                "gallery.html", {"request": request, "user": user, "folders": folders}
            )
    except Exception as e:
        print(f"Problem in gallery: {e}")
        return RedirectResponse('/Photo-Storage')

@router.websocket("/new-folder/ws")
async def new_folder(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            try:
                data = await websocket.receive_json()
                new_folder = data["new_folder"]
                token = data["access_token"]
                username = get_current_user(token[13::])
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