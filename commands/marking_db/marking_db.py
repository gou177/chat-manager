import time

from peewee import *
from playhouse.postgres_ext import JSONField, PostgresqlExtDatabase
from playhouse.sqliteq import SqliteQueueDatabase

db = SqliteQueueDatabase("Marks.db")

class Chat(Model):
    peer_id = IntegerField(null=False)
    
    class Meta:
        database = db
        db_table = "chats"

class Mark(Model):
    mark = TextField(null=False)

    chat = ForeignKeyField(Chat, related_name="marks")
    
    class Meta:
        database = db
        db_table = "marks"

class User(Model):
    user_id = IntegerField(null=False)

    mark = ForeignKeyField(Mark, related_name="users")

    class Meta:
        database = db
        db_table = "users"

def get_chat(peer_id, make_if_none=True):
    try:
        chat = Chat.get(Chat.peer_id == peer_id)
        return chat
    except DoesNotExist:
        if not make_if_none:
            return
        row = Chat(peer_id=peer_id)
        row.save()
        return row

def get_mark(mark, chat, make_if_none=True):
    try:
        m = Mark.get(Mark.mark == mark and Mark.chat == chat)
        return m
    except DoesNotExist:
        if not make_if_none:
            return
        row = Mark(mark=mark, chat=chat)
        row.save()
        return row

def get_user(user_id, mark, make_if_none=True):
    try:
        user = User.get(User.mark == mark and User.user_id == user_id)
        return user
    except DoesNotExist:
        if not make_if_none:
            return
        row = User(mark=mark, user_id=user_id)
        row.save()
        return row

def mark_user(peer_id: int, mark: str, user_id: int):
    c = get_chat(peer_id)
    m = get_mark(mark, c)
    get_user(user_id, m)

def is_user_marked(peer_id: int, mark: str, user_id: int):
    c = get_chat(peer_id, make_if_none=False)
    if c:
        m = get_mark(mark, c, make_if_none=False)
        if m:
            u = get_user(user_id, mark, make_if_none=False)
            if u:
                return True
    return False

def unmark_user(peer_id: int, mark: str, user_id: int):
    c = get_chat(peer_id, make_if_none=False)
    if c:
        m = get_mark(mark, c, make_if_none=False)
        if m:
            u = get_user(user_id, mark, make_if_none=False)
            if u:
                return u.delete_instance()

def initialize():
    Chat.create_table()
    Mark.create_table()
    User.create_table()
    time.sleep(0.5)

initialize()