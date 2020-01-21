# -*- coding: utf-8 -*-
import os
import secrets
import shutil

dev_list = [] # TODO - добавить id всех разработчиков

def isAdmin(store):
    if store.user_id in dev_list:
        return True
    members = store.vk.messages.getConversationMembers(peer_id=store.peer_id)["items"]
    for mem in members:
        if mem.get("is_admin", False) and store.user_id == mem["member_id"]:
            return True
    return False

def remove_folder_contents(path):
    shutil.rmtree(path)
    os.makedirs(path)


def comma(num):
    num = round(int(num))
    return format(num, ',')


def get_token(b=32):
    c_token = secrets.token_urlsafe(b)
    return str(c_token)


def get_smile(num):
    smile = str(num)
    s = {
        1: '1⃣',
        2: '2⃣',
        3: '3⃣',
        4: '4⃣',
        5: '5⃣',
        6: '6⃣',
        7: '7⃣',
        8: '8⃣',
        9: '9⃣',
        0: '0&#8419;'
    }
    for (c, v) in s.items():
        smile = smile.replace(str(c), v)
    return smile


def textify_value(value):
    avalue = abs(value)
    if avalue >= 1000000000000000000000000000000000000000000000000000000000000000:
        return str(round(value / 1000000000000000000000000000000000000000000000000000000000000000, 2)) + " вгтл."
    if avalue >= 1000000000000000000000000000000000:
        return str(round(value / 1000000000000000000000000000000000, 2)) + " дец."
    if avalue >= 1000000000000000000000000000000:
        return str(round(value / 1000000000000000000000000000000, 2)) + " нон."
    if avalue >= 1000000000000000000000000000:
        return str(round(value / 1000000000000000000000000000, 2)) + " окт."
    if avalue >= 1000000000000000000000000:
        return str(round(value / 1000000000000000000000000, 2)) + " сптл."
    if avalue >= 1000000000000000000000:
        return str(round(value / 1000000000000000000000, 2)) + " скст."
    if avalue >= 1000000000000000000:
        return str(round(value / 1000000000000000000, 2)) + " квнт."
    if avalue >= 1000000000000000:
        return str(round(value / 1000000000000000, 2)) + " квдр."
    if avalue >= 1000000000000:
        return str(round(value / 1000000000000, 2)) + " трлн."
    if avalue >= 1000000000:
        return str(round(value / 1000000000, 2)) + " млрд."
    if avalue >= 1000000:
        return str(round(value / 1000000, 2)) + " млн."
    if avalue >= 100000:
        return str(round(value / 100000)) + "00 тыс."
    if avalue >= 1000:
        return str(round(value / 1000)) + " тыс."
    return str(value)
