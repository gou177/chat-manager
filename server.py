import time
from threading import Thread

import requests
import vk_api
import os


from vk_api.bot_longpoll import VkBotMessageEvent, VkBotEventType

from common.Store import api, session
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
                            pass
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
