from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
import bcrypt

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

@router.get("/sign-in/")
async def sign_in(request: Request):
    return tmpl.TemplateResponse("auth/sign_in.html", {"request": request})


@router.post("/sign-in/proccess")
async def sign_in_proccess(
    username: str = Form(...),
    password: str = Form(...)
):
    try: 
        db.connect()
        user = Users.get(Users.username == username)

        if not user:
            raise HTTPException(status_code=404, detail="Account doesn't exist")

        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            raise HTTPException(status_code=400, detail="Invalid login or password")

        token = create_jwt_token({"sub": username})
        
        response = RedirectResponse("/", status_code=303)
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=True,
            samesite="lax"
        )
        return response

    except Users.DoesNotExist:
        raise HTTPException(status_code=404, detail="Account doesn't exist")
    except Exception as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()