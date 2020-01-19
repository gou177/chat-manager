# -*- coding: utf-8 -*-

from utils import *

plugin = EPlugin(theme="aaaaaa")

@plugin.on_command(["online", "онлайн"])
def check(args, store):
    result = "Сейчас онлайн:"
    online = []
    members = store.vk.messages.getConversationMessages(peer_id=store.peer_id)['profiles']
    for mem in members:
        if mem['online']:
            online.append(mem['first_name']+' '+mem['last_name'] + ', ')
    if len(online) == 0:
        result = "Никого нет онлайн"
    else:
        for name in online:
            result += name
        result = result[0:len(result)-2]
    return store.send(result)
    