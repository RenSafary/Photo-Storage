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
                print("Received data:", data)

                token = data["access_token"]
                if "access_token=" in token:
                    token = token.split("access_token=")[1].split(";")[0]
                elif token.startswith("Bearer "):
                    token = token[7:]

                username = get_current_user(token)
                user = Users.get(Users.username == username)

                if Folders.get_or_none((Folders.user == user) & (Folders.name == data["new_folder"])):
                    await websocket.send_json({"status": "error", "detail": "Folder exists"})
                else:
                    Folders.create(name=data["new_folder"], user=user)
                    await websocket.send_json({"status": "success"})

            except WebSocketDisconnect:
                break
            except Exception as e:
                await websocket.send_json({"status": "error", "detail": str(e)})
                await websocket.close(code=1008)
                break

    except Exception as e:
        print("Unexpected error:", e)
    finally:
        await websocket.close()