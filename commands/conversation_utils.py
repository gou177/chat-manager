# -*- coding: utf-8 -*-
from common.Store import Stoaring
from utils import *
from typing import List

plugin = EPlugin(theme="ConversationUtils")


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

@plugin.on_command(["summon", "сбор"])
def summon(args: List[str], store: Stoaring):
    online = False
    result = "\nОбщий сбор!\n"
    if len(args) == 1:
        if "онлайн" in args or "online" in args:
            online = True
    members = store.vk.messages.getConversationMembers(peer_id=store.peer_id)['profiles']
    for mem in members:
        if mem['online'] or not online:
            if 'screen_name' not in mem.keys(): continue # Если человек DELETED
            result += '['+mem['screen_name']+'|'+mem['first_name']+'] '
    return store.send(result)

@plugin.on_command(["mark", "отметь"])
def mark(args: List[str], store: Stoaring):
    store.send("FIXME - функция не завершена")
    i = 0
    while True:
        if len(args) == i:
            break
        if args[0]: pass

@plugin.on_command(["69", "420"])
def nice(args: List[str], store: Stoaring):
    return store.send("Nice")