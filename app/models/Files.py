from peewee import *

from database import connection
from models.Folders import Folders
from models.Tags import Tags

db = connection()

class Files(Model):
    id = AutoField()
    folder = ForeignKeyField(Folders, on_delete="CASCADE", null=True)
    link = CharField()
    date_uploaded = DateField()
    size_of_file_bytes = DoubleField()
    tag = ForeignKeyField(Tags, on_delete="CASCADE", null=True)
    
    class Meta:
        database = db
