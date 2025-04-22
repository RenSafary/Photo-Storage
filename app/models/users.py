from peewee import *

from database import db


class BaseModel(Model):
    class Meta:
        database = db

class Users(Model):
    id = AutoField()
    email = CharField()
    username = CharField()
    password = CharField()