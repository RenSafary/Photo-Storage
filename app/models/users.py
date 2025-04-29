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

class Files(BaseModel):
    id = AutoField()
    user = ForeignKeyField(Users, on_delete="CASCADE")
    link = CharField()    


try:
    db.connect()
    db.create_tables([Users, Files])
except Exception as e:
    print(e)
finally:
    db.close()