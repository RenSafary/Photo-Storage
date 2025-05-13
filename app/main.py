from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import main_page
from routers.auth.sign_in import AuthService
from routers.auth.recover_password import RecoverPassword
from routers.auth import sign_up
from routers.gallery import gallery, folders


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

auth_service = AuthService()
auth_router = auth_service.router

recover_password_service = RecoverPassword()
recover_password_router = recover_password_service.router

app.include_router(main_page.router)
app.include_router(auth_router)
app.include_router(sign_up.router)
app.include_router(recover_password_router)
app.include_router(gallery.router)
app.include_router(folders.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000)