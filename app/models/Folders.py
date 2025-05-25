from peewee import *

from database import connection
from models.Users import Users

db = connection()

class Folders(Model):
    id = AutoField()
    name = CharField()
    user = ForeignKeyField(Users, on_delete="CASCADE")

    class Meta:
        database = db