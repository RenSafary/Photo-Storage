from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import main_page
from routers.auth import sign_in, sign_up, recover_password
from routers.gallery import gallery, upload_files


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(main_page.router)
app.include_router(sign_in.router)
app.include_router(sign_up.router)
app.include_router(recover_password.router)
app.include_router(gallery.router)
app.include_router(upload_files.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000)