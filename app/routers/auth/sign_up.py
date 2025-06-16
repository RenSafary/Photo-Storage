from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import bcrypt
import json

from models.Users import Users, db
from routers.auth.sign_in import AuthService
from redis_client.connection import connect as redis_connection

auth_service = AuthService()

class Sign_Up:
    def __init__(self):
        self.router = APIRouter()
        self.tmpl = Jinja2Templates(directory="./app/templates/")

        self.router.add_api_route("/sign-up", self.sign_up, methods=["GET"])
        self.router.add_api_websocket_route("/sign-up/ws", self.sign_up_ws) 

    async def sign_up(self, request: Request):
        try:
            user = auth_service.verify_token(request)
            if user:
                return RedirectResponse("/Photo-Storage")
            else:
                return self.tmpl.TemplateResponse("auth/sign_up.html", {"request": request})
        except Exception as e:
            print(f"Error in sign_up: {e}")
            return RedirectResponse("/Photo-Storage")

    async def sign_up_ws(self, websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                try:
                    data = await websocket.receive_json()

                    email = data["email"]
                    username = data["username"]
                    password = data["password"]
                    repeat_pass = data["repeat_pass"]

                    if password != repeat_pass:
                        await websocket.send_json(
                            {"status": "error", "detail": "Passwords don't match"}
                        )
                        continue

                    salt = bcrypt.gensalt()
                    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

                    try:
                        db.connect()

                        if Users.get_or_none(Users.username == username):
                            await websocket.send_json(
                                {"status": "error", "detail": "Username already taken"}
                            )
                            continue

                        if Users.get_or_none(Users.email == email):
                            await websocket.send_json(
                                {"status": "error", "detail": "Email already registered"}
                            )
                            continue

                        Users.create(
                            email=email,
                            username=username,
                            password=hashed_password.decode("utf-8")
                        )
                        user_id = Users.get_id(username=username)
                        # authorization
                        token = auth_service.create_jwt_token({"sub": username})

                        # redis
                        user_data = {
                            "id": user_id,
                            "email": email,
                            "username": username
                        }
                        rdb = redis_connection()
                        rdb.setex(f"user_id:{user_data["id"]}", 3600, json.dumps(user_data))

                        await websocket.send_json({"status": "success", "token": token})
                        break

                    except Exception as e:
                        print(f"Database error: {e}")
                        await websocket.send_json(
                            {"status": "error", "detail": "Registration failed"}
                        )

                except json.JSONDecodeError:
                    await websocket.send_json(
                        {"status": "error", "detail": "Invalid data format"}
                    )
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    await websocket.send_json(
                        {"status": "error", "detail": "Internal server error"}
                    )
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
        except WebSocketDisconnect:
            print("Connection is closed")
        finally:
            try:
                await websocket.close()
            except:
                pass
            if not db.is_closed():
                db.close()
