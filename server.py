from threading import Thread

import json
import os
import re
import requests
import sys
from vk_api.bot_longpoll import VkBotMessageEvent, VkBotEventType

from common.Store import *


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



