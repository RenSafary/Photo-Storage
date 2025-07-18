from peewee import *

from database import connection
from models.Folders import Folders
from models.Users import Users

db = connection()

class Files(Model):
    id = AutoField()
    user = ForeignKeyField(Users, on_delete="CASCADE")
    folder = ForeignKeyField(Folders, on_delete="CASCADE", null=True)
    link = CharField()
    date_uploaded = DateField()
    size_of_file_bytes = DoubleField()
    
    class Meta:
        database = db
