# -*- coding: utf-8 -*-
from common.Store import Stoaring
from utils import *

plugin = EPlugin(theme="aaaaaa")


@plugin.on_command(["online", "онлайн"])
def check(args, store: Stoaring):
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
