from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

tmpl = Jinja2Templates(directory="./app/templates")

@router.get("/")
async def main_page(request: Request):
    return tmpl.TemplateResponse("main.html", {'request': request})