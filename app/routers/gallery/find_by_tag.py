from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
import jwt

from routers.auth.sign_in import AuthService
from models.Users import Users
from models.Folders import Folders
from models.Files import Files
from models.Tags import Tags


auth = AuthService()

class Find_By_Tag:
    def __init__(self):
        self.router = APIRouter()
        self.template = Jinja2Templates(directory="./app/templates/gallery/")

        self.router.add_api_route("/find-by-tag/", self.main_page, methods=["GET"])
        self.router.add_api_websocket_route("/find-tag/ws", self.find_tag)

    def get_current_user(self, token: str):
        load_dotenv()

        SECRET_KEY = os.getenv("SECRET_KEY")
        ALGORITHM = os.getenv("ALGORITHM")

        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username = payload.get("sub")

        return username


    async def main_page(self, request: Request):
        user = auth.verify_token(request)
        if not user:
            return HTMLResponse(content="<H1>Forbidden. Not authorized</H1>")
        else:
            user_db = Users.get(Users.username == user)
            tags = Tags.select().where(Tags.user == user_db.id)
            files = Files()
            return self.template.TemplateResponse(request, "find_by_tag.html", {"tags": tags, 'files': files})
    
    async def find_tag(self, websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                try:
                    data = await websocket.receive_json()
                    name = data["tag"]
                    token = data["token"]
                    user = self.get_current_user(token[13::])

                    user = Users.get_or_none(Users.username == user)

                    if user is None:
                        await websocket.send_json({
                            "status": "error",
                            "detail": "User not found"
                        })
                        await websocket.close()
                        return

                    tags_list = []
                    query = Tags.select().where(
                    (Tags.user == user.id) & 
                    (Tags.name.contains(name)))
                
                    for tag in query:
                        tags_list.append(tag.name)

                    await websocket.send_json({
                        "status":"success",
                        "tags_list": tags_list
                    })
                except Exception:
                    await websocket.send_json({
                        "status":"error",
                        "detail":"Internal server error"
                    })
                    print(f"Error: {str(e)}")
                    await websocket.close()
                    return

        except WebSocketDisconnect as wsd:
            print(wsd)
        except Exception as e:
            print("Error in tags", str(e))
        finally:
            try:
                await websocket.close()
            except:
                pass
        