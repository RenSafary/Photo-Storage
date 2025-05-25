from fastapi import APIRouter, Request, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
import bcrypt
import json

from models.Users import Users, db

load_dotenv()

class AuthService:
    def __init__(self):
        self.router = APIRouter()
        self.templates = Jinja2Templates(directory="./app/templates/")
        self.secret_key = os.environ.get("SECRET_KEY")
        self.algorithm = os.environ.get("ALGORITHM")
        self.token_expire_minutes = 1440
        
        self.router.add_api_route("/sign-in/", self.sign_in, methods=["GET"])
        self.router.add_api_websocket_route("/sign-in/ws", self.sign_in_ws)

    def create_jwt_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.token_expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, request: Request):
        token = request.cookies.get("access_token") or request.headers.get("authorization")
        if not token:
            return None
        if token.startswith("Bearer "):
            token = token[7:]

        try:
            payload = jwt.decode(token, self.secret_key, algorithms=self.algorithm)
            username = payload.get("sub")
            if not username:
                raise HTTPException(status_code=401, detail="Invalid token")
            return username
        except JWTError as e:
            raise HTTPException(status_code=401, detail=f"Token error: {str(e)}")

    async def sign_in(self, request: Request):
        try:
            user = self.verify_token(request)
            if user:
                return RedirectResponse("/Photo-Storage")
            else:
                return self.templates.TemplateResponse("auth/sign_in.html", {"request": request})
        except Exception as e:
            print(f"Error in sign_in function: {e}")
            return RedirectResponse("/Photo-Storage")

    async def sign_in_ws(self, websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                try:
                    data = await websocket.receive_json()
                    
                    username = data['username']
                    password = data['password']

                    db.connect()
                    try:
                        user = Users.get(Users.username == username)
                        
                        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                            await websocket.send_json({'status': 'error', 'detail': 'Wrong password'})
                            continue

                        token = self.create_jwt_token({"sub": username})
                        
                        await websocket.send_json({
                            'status': 'success',
                            'token': token
                        })
                        break
                        
                    except Users.DoesNotExist:
                        await websocket.send_json({'status': 'error', 'detail': 'Account doesn\'t exist'})
                    except Exception as e:
                        await websocket.send_json({'status': 'error', 'detail': 'Internal server error'})
                        print(f"Error: {str(e)}")
                    finally:
                        if not db.is_closed():
                            db.close()
                            
                except json.JSONDecodeError:
                    await websocket.send_json({'status': 'error', 'detail': 'Invalid data format'})
                    
        except WebSocketDisconnect:
            print("Client disconnected")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
        finally:
            try:
                await websocket.close()
            except:
                pass
            if not db.is_closed():
                db.close()