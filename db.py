from peewee import *
from playhouse.postgres_ext import JSONField, PostgresqlExtDatabase
from playhouse.sqliteq import SqliteQueueDatabase
from common import Logger
import datetime

# db = PostgresqlDatabase('',
#                         user='',
#                         password='',
#                         host='',
#                         port=0)


db = SqliteQueueDatabase("Test.db")


class Global(Model):
    id = PrimaryKeyField(null=False)
    user_id = IntegerField(null=False)
    ban = IntegerField(default=0)
    prefix = TextField(default='')

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
        raise
