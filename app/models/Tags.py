from peewee import *

from database import connection
from models.Users import Users

db = connection()

class Tags(Model):
    id = AutoField()
    name = CharField()
    user = ForeignKeyField(Users, on_delete="CASCADE")
    #count = IntegerField()
    class Meta:
        database = db
