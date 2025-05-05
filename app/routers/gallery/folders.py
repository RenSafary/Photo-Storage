from fastapi import APIRouter, Request, UploadFile, File, Form, HTTPException
from fastapi.exceptions import HTTPException
from typing import List
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates


from routers.auth.sign_in import verify_token
from models import Users, Folders, Files
from utils.storage.get_files import get_files
from utils.storage.upload_files import upload_files
from utils.storage.delete_file import delete_s3_file

router = APIRouter()

tmpl = Jinja2Templates(directory="./app/templates/gallery/")


@router.get("/folder/{username}/{folder_name}")
async def in_folder(
    username: str, 
    folder_name: str, 
    request: Request
):
    try:
        current_user = verify_token(request)
        
        if username != current_user:
            return HTMLResponse(
                content="<h1>403 Forbidden</h1><p>You don't have access to this folder</p>",
                status_code=403
            )
        
        user = Users.get(Users.username == current_user)
        folder = Folders.get_or_none(
            (Folders.user == user.id) & 
            (Folders.name == folder_name)
        )
        
        if not folder:
            return HTMLResponse(
                content=f"<h1>404 Not Found</h1><p>Folder '{folder_name}' doesn't exist</p>",
                status_code=404
            )
        
        # realization getting files from storage
        files = get_files(user.username, folder.name)
        
        return tmpl.TemplateResponse(
            "folders.html",
            {
                "request": request,
                "user": current_user,
                "folder_name": folder_name,
                "folder": folder,
                "files": files 
            }
        )
        
    except HTTPException:
        raise
        
    except Exception as e:
        print(f"Error in folder view: {str(e)}")
        return HTMLResponse(
            content=f"<h1>500 Server Error</h1><p>{str(e)}</p>",
            status_code=500
        )

@router.post("/folder/{username}/{folder_name}/uploading/")
async def upload_files_to_storage(
    username: str,
    folder_name: str,
    media_file: List[UploadFile] = File(...),
):
    username_db = Users.get(username=username)
    folder_db = Folders.get(user=username_db.id, name=folder_name)

    for file in media_file:
        if not file:
            print("X")
        else:
            file_path = f"{username}/{folder_name}/{file.filename}"
            upload_files(file_path, file)
            file_path_db = Files.create(folder=folder_db.id, link=file_path)
    return RedirectResponse(f"/folder/{username}/{folder_name}/")

@router.post("/delete/")
async def delete_file(
    file_path: str = Form(...)
):
    response = delete_s3_file(file_path)
    if response.status_code == 200:
        return RedirectResponse("/gallery")
    else:
        return HTMLResponse(f"<H1>{response.status_code}</H1><p>{response.content}</p>")