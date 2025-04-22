from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import psycopg2
from psycopg2 import sql

from database import create_connection

router = APIRouter()

tmpl = Jinja2Templates(directory="./app/templates/")


@router.get("/sign-up")
async def sign_up(request: Request):
    return tmpl.TemplateResponse("sign_up.html", {"request": request})


@router.post("/sign-up/proccess")
async def sign_up_proccess(
    username: str = Form(...), password: str = Form(...), email: str = Form(...)
):
    conn = create_connection()
    try: 
        with conn.cursor() as cursor:
            insert_query = sql.SQL("""
            INSERT INTO users(username, password)
            VALUES(%s, %s)
        """)
            cursor.execute(insert_query, (username, password))
            conn.commit()
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": e})
    return JSONResponse({"username": username, "password": password, "email": email})
