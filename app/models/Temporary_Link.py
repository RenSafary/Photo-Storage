from peewee import *

from models.Users import Users
from models.Files import Files
from database import connection


db = connection()

class Temp_Link(Model):
    id = AutoField()
    user = ForeignKeyField(Users, on_delete="CASCADE")
    file = ForeignKeyField(Files, on_delete="CASCADE")
    expired_at = DateField()
    
    class Meta:
        database = db