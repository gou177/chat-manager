# -*- coding: utf-8 -*-
from common.Store import Stoaring
from utils import *
import requests

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
        if profile['is_closed'] == True: # Проверка на то, открыта страница или нет
            check_close = 'закрытая'
        if profile['sex'] == 1:
            sex = 'Ж'

        mem_list.append(f"[id{profile['id']}|{profile['first_name']} {profile['last_name']}] - {sex}, {check_close} стр, vkid - {profile['screen_name']}")

    msg += "\n".join(mem_list)
    return store.send(msg)


@plugin.on_command(['id', 'ид'])
def id_user(args: list, store: Stoaring):
    try:
        user_id = store.event.obj['reply_message']['from_id']
        return store.send(f'id пользователя: {user_id}')
    except KeyError:
        return store.send(f'ваш id: {store.user_id}')


@plugin.on_command(["kick", "кик"])
def kickuser(args: list, store: Stoaring):
    try:
        user_id = store.event.obj['reply_message']['from_id']
        kickid = store.vk.messages.removeChatUser(chat_id=store.event.chat_id, member_id=user_id)
        return store.send('я молодец, я кикнул его из беседы &#128570;')
    except KeyError:
        return store.send('возникла ошибка. Разраб рукожоп!')

### TODO до лучших дней
# @plugin.on_command(["pin", "закреп"])
# def pinit(args: list, store: Stoaring):
#     pin = store.vk.messages.pin(peer_id=store.peer_id, message_id=store.event.obj['reply_message']['id'])
#     return store.send('я молодец, я закрепил сообщение &#128570;')


@plugin.on_command(["whois", "ктоты"])
def whoru(args: list, store: Stoaring):
    try:
        fields = ['verified', 'city', 'country', 'timezone']
        user_id = store.event.obj['reply_message']['from_id'] # Получаем id пользователя
        get = store.vk.users.get(user_id=user_id, fields=fields, name_case='nom')[0]

        get_xml = requests.get(f'https://vk.com/foaf.php?id={user_id}').text.split() # Запрос к серверу VK
        xml_data = []
        for xml in get_xml:
            if 'dc:date' in xml: # Поиск дат
                xml_data.append(xml[xml.index('2'):xml.index('T')]) # Добавление найденной даты с лис
        dreg = xml_data[0]

        name = get['first_name'] + ' ' + get['last_name']
        date_of_reg = dreg[8:10] + '.' + dreg[5:7] + '.' + dreg[0:4] # Собираем дату по частям
        
        return store.send(f'\nИмя: {name} \nДата регистрации: {date_of_reg}')
    except Exception as e:
        print('Error:', e)
        return store.send('мне нужно сообщение человека, про которого вы хотите узнать.')
    

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