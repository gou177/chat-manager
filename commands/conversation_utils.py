# -*- coding: utf-8 -*-
from common.Store import Stoaring
from utils import *
from typing import List
import json

plugin = EPlugin(theme="ConversationUtils")

try:
    file = open("marks.json")
    data = json.load(file)
    file.close()
except FileNotFoundError:
    data = {}

def updateData():
    file = open("marks.json", 'w')
    json.dump(data, file)
    file.close()

"""
@plugin.on_command(["online", "онлайн"])
def check(args: List[str], store: Stoaring):
    msg = "\nСейчас онлайн: "
    online = []
    members = store.vk.messages.getConversationMembers(peer_id=store.peer_id)['profiles']
    for mem in members:
        if mem['online']:
            online.append(f"{mem['first_name']} {mem['last_name']}")

    if len(online) == 0:
        return store.send("Никого нет онлайн")

    msg += "\n".join(online)
    return store.send(msg)
"""

@plugin.on_command(["summon", "сбор"])
def summon(args: List[str], store: Stoaring):
    online = False
    if len(args) == 0: result = start_result = "\nОбщий сбор!\n"
    else:
        result = "Общий сбор среди тех, кто "
        if len(args) > 1:
            for i in range(len(args) - 1):
                result += args[i] + ", "
            result += 'и ' + args[len(args) - 1] + "!\n"
        else:
            result += args[0] + "!\n"
        start_result = result
    marks = []
    for arg in args:
        if arg in ("online", "онлайн"): online = True
        else: marks.append(arg)
    members = store.vk.messages.getConversationMembers(peer_id=store.peer_id)['profiles']
    for mem in members:
        mem_marks = data.get(str(store.peer_id), {}).get(str(mem["id"]), [])
        if (mem['online'] or not online) and all([mark in mem_marks for mark in marks]):
            if 'screen_name' not in mem.keys(): continue # Если человек DELETED
            result += '['+mem['screen_name']+'|'+mem['first_name']+'] '
    if result == start_result: return store.send("По данным аргументам никого не найдено")
    return store.send(result)

@plugin.on_command("mark")
def mark(args: List[str], store: Stoaring):
    if len(args) < 2:
        return store.send("Неправильное использование команды\n\nИспользование: /mark <id> <отметка>")
    else:
        if args[0].startswith('@'):
            args[0] = args[0][1:]
        vk_id = None
        try:
            vk_id = store.vk.utils.resolveScreenName(screen_name=args[0])["object_id"]
        except KeyError:
            store.send("Неправильный id. Убедитесь, что id - не ссылка, или попробуйте без @ или *")
            return
        
        vk_id = str(vk_id)
        peer_id = str(store.peer_id)
        # JSON не хранит int как ключи, из-за чего могут быть проблемы

        data[peer_id] = data.get(peer_id, {})
        data[peer_id][vk_id] = data[peer_id].get(vk_id, [])
        if not args[1] in data[peer_id][vk_id]:
            data[peer_id][vk_id].append(args[1])
            store.send("Отметка успешно поставлена")
        else:
            store.send("Отметка уже стоит")
        updateData()

@plugin.on_command("unmark")
def mark(args: List[str], store: Stoaring):
    if len(args) < 2:
        return store.send("Неправильное использование команды\n\nИспользование: /unmark <id> <отметка>")
    else:
        if args[0].startswith('@'):
            args[0] = args[0][1:]
        vk_id = None
        try:
            vk_id = store.vk.utils.resolveScreenName(screen_name=args[0])["object_id"]
        except KeyError:
            store.send("Неправильный id. Убедитесь, что id - не ссылка, или попробуйте без @ или *")
            return
        
        vk_id = str(vk_id)
        peer_id = str(store.peer_id)
        # JSON не хранит int как ключи, из-за чего могут быть проблемы

        data[peer_id] = data.get(peer_id, {})
        data[peer_id][vk_id] = data[peer_id].get(vk_id, [])
        if args[1] in data[peer_id][vk_id]:
            data[peer_id][vk_id].remove(args[1])
            store.send("Отметка успешно удалена")
        else:
            store.send("Отметка отсутствует")
        updateData()

@plugin.on_command(["69", "420"])
def nice(args: List[str], store: Stoaring):
    return store.send("Nice")