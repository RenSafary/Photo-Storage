from peewee import *

def connection():
    return SqliteDatabase("./db.sqlite")