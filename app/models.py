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
    recover_link = CharField(null=True)
    recover_link_expires = DateTimeField(null=True)

class Folders(BaseModel):
    id = AutoField()
    name = CharField()
    user = ForeignKeyField(Users, on_delete="CASCADE")


class Files(BaseModel):
    id = AutoField()
    folder = ForeignKeyField(Folders, on_delete="CASCADE")
    link = CharField()
    date_uploaded = DateField()
    size_of_file_bytes = DoubleField()
  

try:
    db.connect()
    db.create_tables([Users, Folders, Files])
except Exception as e:
    print(e)
finally:
    db.close()