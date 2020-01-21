# -*- coding: utf-8 -*-
from common.Store import Stoaring
from utils import *

plugin = EPlugin(theme="ConvUtils")


@plugin.on_command(["online", "онлайн"])
def check(args: list, store: Stoaring):
    msg = "\nСейчас онлайн:\n"
    online = []
    members = store.vk.messages.getConversationMembers(peer_id=store.peer_id)
    profiles = members['profiles']
    for mem in profiles:
        if 'is_mobile' in mem['online_info']:
            online.append(f"{mem['first_name']} {mem['last_name']} с телефона &#128241;")
        elif mem['online']:
            online.append(f"{mem['first_name']} {mem['last_name']}")
 
    #print(online)
    if len(online) == 0:
        return store.send("Никого нет онлайн")

    msg += "\n".join(online)
    return store.send(msg)


@plugin.on_command(["members", "участники"])
def check(args: list, store: Stoaring):
    msg = "\nУчастники беседы:\n"
    mem_list = []
    check_close = 'открытая'
    sex = 'М'
    members = store.vk.messages.getConversationMembers(peer_id=store.peer_id)
    profiles = members['profiles']
    for profile in profiles:
        #print(profile)
        if profile['is_closed']:
            check_close = 'закрытая'
        if profile['sex'] == 1:
            sex = 'Ж'

        mem_list.append(f"{profile['first_name']} {profile['last_name']} - {sex}, {check_close} стр, vkid - {profile['screen_name']}")

    msg += "\n".join(mem_list)
    return store.send(msg)

@plugin.on_command(["summon", "сбор"])
def summon(args: list, store: Stoaring):
    online = False
    result = "\nОбщий сбор!\n"
    if len(args) == 1:
        if "онлайн" in args or "online" in args:
            online = True
    members = store.vk.messages.getConversationMembers(peer_id=store.peer_id)['profiles']
    for mem in members:
        if mem['online'] or not online:
            if 'screen_name' not in mem: return # Если человек DELETED
            result += '['+mem['screen_name']+'|'+mem['first_name']+'] '
    return store.send(result)