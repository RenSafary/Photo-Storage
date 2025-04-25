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


try:
    db.connect()
    db.create_tables([Users])
except Exception as e:
    print(e)
finally:
    db.close()