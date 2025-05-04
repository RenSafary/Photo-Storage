from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.websockets import WebSocket
from jose import jwt
from dotenv import load_dotenv
import os

from routers.auth.sign_in import verify_token
from utils.storage.get_files import get_files
from models.users import Users, Folders


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
async def files(request: Request):
    files = get_files()
    username = verify_token(request)

    user = Users.get(Users.username == username)
    folders = Folders.select().where(Folders.user == user.id)

    return tmpl.TemplateResponse(
        "gallery.html", {"request": request, "user": user, "folders": folders}
    )


@router.websocket("/new-folder/ws")
async def new_folder(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            new_folder = data["new_folder"]

            token = data["access_token"]
            username = get_current_user(token[13::])

            user = Users.get(Users.username == username)

            if Folders.get_or_none(
                (Folders.user == user) & (Folders.name == new_folder)
            ):
                await websocket.send_json(
                    {"status": "error", "details": "Folder name is already taken"}
                )
                # return
            else:
                folder = Folders.create(name=new_folder, user=user.id)
                await websocket.send_json({"status": "success", "token": token})
                # return
    except Exception as e:
        print("Error in gallery.py websocket:", e)
        await websocket.send_json(
            {"status": "error", "detail": "Internal server error"}
        )
        await websocket.close()
