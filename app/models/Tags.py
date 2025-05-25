from peewee import *

from database import connection

db = connection()

class Tags(Model):
    id = AutoField()
    name = CharField()
    count = IntegerField()
    class Meta:
        database = db
