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
    chat = Chat.get_or_none(Chat.peer_id == peer_id)
    if chat or not make_if_none:
        return chat
    else:
        chat = Chat(peer_id=peer_id)
        chat.save()
        return chat

def get_mark(mark, chat, make_if_none=True):
    m = Mark.get_or_none(Mark.mark == mark, Mark.chat == chat)
    if m or not make_if_none:
        return m
    else:
        m = Mark(mark=mark, chat=chat)
        m.save()
        return m

def get_user(user_id, mark, make_if_none=True):
    user = User.get_or_none(User.mark == mark, User.user_id == user_id)
    if user or not make_if_none:
        return user
    else:
        user = User(mark=mark, user_id=user_id)
        user.save()
        return user

def mark_user(peer_id: int, mark: str, user_id: int):
    c = get_chat(peer_id)
    m = get_mark(mark, c)
    get_user(user_id, m)

def is_user_marked(peer_id: int, mark: str, user_id: int):
    c = get_chat(peer_id, make_if_none=False)
    if c:
        m = get_mark(mark, c, make_if_none=False)
        if m:
            u = get_user(user_id, m, make_if_none=False)
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

def delete_mark(peer_id: int, mark: str):
    c = get_chat(peer_id, make_if_none=False)
    if c:
        m = get_mark(mark, c, make_if_none=False)
        if m:
            for u in User.select().where(User.mark == m):
                u.delete_instance()
            m.delete_instance()
            return True
    return False

def initialize():
    try:
        db.connect()
        Chat.create_table()
        Mark.create_table()
        User.create_table()
        time.sleep(0.5)
    except InternalError as px:
        print(str(px))
        raise

initialize()