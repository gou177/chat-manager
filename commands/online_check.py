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
            online.append(f"{mem['first_name']} {mem['last_name']} &#128241;")
        elif mem['online']:
            online.append(f"{mem['first_name']} {mem['last_name']} &#128187;")
 
    #print(online)
    if len(online) == 0:
        return store.send("Никого нет онлайн")

    msg += "\n".join(online)
    return store.send(msg)



@plugin.on_command(["members", "участники"])
def check(args: list, store: Stoaring):
    msg = "\nУчастники беседы:\n"
    mem_list = []
    members = store.vk.messages.getConversationMembers(peer_id=store.peer_id)
    profiles = members['profiles']
    for profile in profiles:
        check_close = 'открытая'
        sex = 'М'
        print(profile)
        if profile['is_closed'] == True:
            check_close = 'закрытая'
        if profile['sex'] == 1:
            sex = 'Ж'

        mem_list.append(f"[id{profile['id']}|{profile['first_name']} {profile['last_name']}] - {sex}, {check_close} стр, vkid - {profile['screen_name']}")

    msg += "\n".join(mem_list)
    return store.send(msg)

@plugin.on_command(["fakea", "типоаудио"])
def fakeaudio(args: list, store: Stoaring):
    return store.vk.messages.setActivity(user_id=store.user_id , type='audiomessage', peer_id=store.peer_id, group_id=191058623)


@plugin.on_command(["deletephoto", "удалитьфото"])
def delphotos(args: list, store: Stoaring):
    delphoto = store.vk.messages.deleteChatPhoto(chat_id=store.event.chat_id, group_id=store.event.group_id)
    return store.send('я молодец, я удалил фото беседы &#128570;')


@plugin.on_command(["changename", "сменитьназвание"])
def changenameo(args: list, store: Stoaring):
    print(args)
    changen = store.vk.messages.editChat(chat_id=store.event.chat_id, title=' '.join(args))
    return store.send('я молодец, я сменил название беседы &#128570;')

### TODO до лучших дней
# @plugin.on_command(["pin", "закреп"])
# def pinit(args: list, store: Stoaring):
#     pin = store.vk.messages.pin(peer_id=store.peer_id, message_id=store.event.obj['reply_message']['id'])
#     return store.send('я молодец, я закрепил сообщение &#128570;')


# @plugin.on_command(["whois", "ктоты"])
# def whoru(args: list, store: Stoaring):
#     get = store.vk.users.get(user_id=store.event.obj['reply_message']['from_id'], fields=['verified', 'bdate', 'city', 'country', 'status','timezone'], name_case='nom')
#     print(get)



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