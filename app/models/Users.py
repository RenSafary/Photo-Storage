from peewee import *

from database import connection

db = connection()

class Users(Model):
    id = AutoField()
    email = CharField()
    username = CharField()
    password = CharField()
    recover_link = CharField(null=True)
    recover_link_expires = DateTimeField(null=True)

    class Meta:
        database = db 