# -*- coding: utf-8 -*-
from common.Store import Stoaring
from utils import *

plugin = EPlugin(theme="ConvUtils")


@plugin.on_command(["online", "онлайн"])
def check(args: list, store: Stoaring):
    msg = "\nСейчас онлайн:"
    online = []
    members = store.vk.messages.getConversationMessages(peer_id=store.peer_id)['profiles']
    for mem in members:
        if mem['online']:
            online.append(f"{mem['first_name']} {mem['last_name']}")

    if len(online) == 0:
        return store.send("Никого нет онлайн")

    msg += "\n".join(online)
    return store.send(msg)

@plugin.on_command(["summon", "сбор"])
def summon(args: list, store: Stoaring):
    online = False
    result = "\nОбщий сбор!\n"
    if len(args) == 1:
        if "онлайн" in args or "online" in args:
            online = True
    members = store.vk.messages.getConversationMessages(peer_id=store.peer_id)['profiles']
    for mem in members:
        if mem['online'] or not online:
            if 'screen_name' not in mem.keys: return # Если человек DELETED
            result += '['+mem['screen_name']+'|'+mem['first_name']+'] '
    store.send(result)