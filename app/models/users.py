from peewee import *

db = SqliteDatabase("./db.sqlite")

class BaseModel(Model):
    class Meta:
        database = db

class Users(BaseModel):
    id = AutoField()
    email = CharField()
    username = CharField()
    password = CharField()


try:
    db.connect()
    db.create_tables([Users])
except Exception as e:
    print(e)
finally:
    db.close()