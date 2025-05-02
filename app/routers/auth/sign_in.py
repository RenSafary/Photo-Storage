from fastapi import APIRouter, Request, HTTPException, WebSocket
from fastapi.templating import Jinja2Templates
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
import bcrypt
import json

from models.users import Users, db

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()

tmpl = Jinja2Templates(directory="./app/templates/")

def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(request: Request):
    token = request.cookies.get("access_token") or request.headers.get("authorization")
    if not token:
        return None
    if token.startswith("Bearer "):
        token = token[7:]

    try:
        # getting username
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token error: {str(e)}")

@router.get("/sign-in/")
async def sign_in(request: Request):
    return tmpl.TemplateResponse("auth/sign_in.html", {"request": request})


@router.websocket("/sign-in/ws")
async def sign_in_proccess(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_json()
        
        username = data['username']
        password = data['password']

        db.connect()
        try:
            user = Users.get(Users.username == username)
            
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                await websocket.send_json({'status': 'error', 'detail': 'Wrong password'})
                return

            token = create_jwt_token({"sub": username})
            
            await websocket.send_json({
                'status': 'success',
                'token': token
            })     
            
        except Users.DoesNotExist:
            await websocket.send_json({'status': 'error', 'detail': 'Account doesn\'t exist'})
            
    except json.JSONDecodeError:
        await websocket.send_json({'status': 'error', 'detail': 'Invalid data format'})
    except Exception:
        await websocket.send_json({'status': 'error', 'detail': 'Internal server error'})
    finally:
        if not db.is_closed():
            db.close()