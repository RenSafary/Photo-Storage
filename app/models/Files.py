from peewee import *

from database import connection
from models.Folders import Folders

db = connection()

class Files(Model):
    id = AutoField()
    folder = ForeignKeyField(Folders, on_delete="CASCADE")
    link = CharField()
    date_uploaded = DateField()
    size_of_file_bytes = DoubleField()
    
    class Meta:
        database = db