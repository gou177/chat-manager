# -*- coding: utf-8 -*-
from common.Store import Stoaring
from utils import *

plugin = EPlugin(theme="ConvUtils")


@plugin.on_command(["fakea", "типоаудио"])
def fakeaudio(args: list, store: Stoaring):
    return store.vk.messages.setActivity(user_id=store.user_id , type='audiomessage', peer_id=store.peer_id, group_id=191058623)


@plugin.on_command(["deletephoto", "удалитьфото"])
def delphotos(args: list, store: Stoaring):
    delphoto = store.vk.messages.deleteChatPhoto(chat_id=store.event.chat_id, group_id=store.event.group_id)
    return store.send('я молодец, я удалил фото беседы &#128570;')


@plugin.on_command(["changename", "сменитьназвание"])
def changenameo(args: list, store: Stoaring):
    changen = store.vk.messages.editChat(chat_id=store.event.chat_id, title=' '.join(args))
    return store.send('я молодец, я сменил название беседы &#128570;')
