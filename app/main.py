from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import sign_in, sign_up
#from models.users import Users
#from database import db


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(sign_in.router)
app.include_router(sign_up.router)

"""try:
    db.connect()
    db.create_tables([Users])
except Exception as e:
    print(e)
finally:
    db.close()"""

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000)