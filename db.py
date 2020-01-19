from peewee import *
from playhouse.postgres_ext import JSONField, PostgresqlExtDatabase
from common import Logger
import datetime

db = PostgresqlDatabase('',
                        user='',
                        password='',
                        host='',
                        port=0)


# db = SqliteDatabase("Test.db")

class Global(Model):
    id = PrimaryKeyField(null=False)
    user_id = IntegerField(null=False)


    class Meta:
        db_table = 'global'
        database = db


def con():
    try:
        db.connect()
        Global.create_table()
        Logger.Blog('База данных загружена')
    except InternalError as px:
        print(str(px))
