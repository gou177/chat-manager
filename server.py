# -*- coding: utf-8 -*-
import json
import time
from threading import Thread

import requests
import vk_api
import os
import re

from vk_api.bot_longpoll import VkBotMessageEvent, VkBotEventType

from common.Store import api, session, Stoaring
from db import *


class Command:
    def __init__(self):
        self.cmd = {}
        self.cmd_p = {}

    def get(self):
        services = os.listdir('commands')
        service_classes = {}
        import commands as com
        for service in services:
            if service.endswith('.py') and service != '__init__.py':
                module = eval(f'com.{service[:-3]}').plugin
                service_classes[module.theme] = [module.cmd, module.cmd_p]
                for c, v in module.cmd.items():
                    self.cmd[c] = v
                for c, v in module.cmd_p.items():
                    self.cmd_p[c] = v
                Logger.Glog(f'Плагин {Logger.RED}[{module.theme}]{Logger.GREEN} загружен')

        return service_classes


class Longpoll:

    def __init__(self):

        con()
        self.vk = api
        self.prefixes = ['.', '/']
        self.command = Command()
        self.command.get()
        self.settings = self.vk.groups.getById()
        self.group_id = self.settings[0]['id']
        self.ex = 0

    def setLP(self):
        self.longpoll = vk_api.bot_longpoll.VkBotLongPoll(session, self.group_id)

    def start(self):
        self.setLP()
        Logger.Ylog(f'Бот запущен.\n'
                    f'Группа https://vk.com/club{self.group_id}')
        while True:
            try:
                for event in self.longpoll.listen():
                    if event.type == VkBotEventType.MESSAGE_NEW:
                        if event.obj.from_id > 0:
                            ctx = Stoaring(event).init()
                            if ctx.alive:
                                if 'payload' in event.obj:

                                    p = json.loads(event.obj['payload'])
                                    if "command" in p:
                                        if p['command'] in self.command.cmd_p:
                                            Logger.Pulselog(
                                                f"{p['command']} | {f'USSR: {event.obj.peer_id}' if not event.from_chat else f'ChAT: #{event.chat_id}, | USSR: {event.obj.from_id}'}")
                                            Thread(target=self.command.cmd_p[p['command']][0],
                                                   args=[[], ctx],
                                                   daemon=True).start()
                                            continue
                                command, args = self.check_command(event.obj.text)
                                if command:
                                    Logger.Pulselog(
                                        f"{command} | {args} | {f'USSR: {event.obj.peer_id}' if not event.from_chat else f'ChAT: #{event.chat_id}, | USSR: {event.obj.from_id}'}")
                                    self.command.cmd[command][0](args, ctx)
                                    continue

            except requests.exceptions.ReadTimeout:
                pass
            except requests.exceptions.ConnectionError:
                self.ex += 1
                if self.ex > 10:
                    Logger.Wlog('requests.exceptions.ConnectionError')
                    self.ex = 0
                    time.sleep(3600)
                    self.setLP()
                    Logger.Ylog('Едем дальше')
            except Exception as s:
                Logger.Rlog(f'{s.__class__} {s}')
                raise

    def check_command(self, text):
        text = re.sub(r"^\[club\d+\|.+\]", '', text).strip()
        text = text.lower()
        if len(text) == 0:
            return False, False

        for p in self.prefixes:
            if text.startswith(p):
                text = text[len(p):] + ' '
                break
        else:
            return False, False

        if len(text.split()) == 0: return False, False
        for comm in self.command.cmd:
            if comm == text.split()[0]:
                return comm, text.split()[1:]
        return False, False