import time
from threading import Thread

from common import Logger
from common.Store import st


class EPlugin:
    __version__ = '1.0'

    def __init__(self, theme):
        self.theme = theme
        self.cmd = {}
        self.cmd_p = {}

    def on_command(self, command=None, payload=None):
        def wrapper(func):
            if payload is not None:
                if 'command' in payload:
                    self.cmd_p[payload['command']] = [func]
                else:
                    raise IndexError('ДЕбил блять укажи нормальную команду в Жсон')

            if command is not None:
                if type(command) in (list, tuple):
                    for comm in command:
                        self.cmd[comm] = [func]
                else:
                    self.cmd[command] = [func]

            return func

        return wrapper

    def timing(self, t, wait=None):
        def wrapper(func):
            thread_new = Thread(target=self.sh, args=[func, t, wait], daemon=True)
            Logger.Plog(f'Shedule: {t}')
            thread_new.start()

            return func

        return wrapper

    @staticmethod
    def sh(func, t, wait):
        if wait:
            time.sleep(wait)
        while True:
            try:
                func(st)
            except Exception as s:
                print(s)
            finally:
                time.sleep(t)

    def start(self, name):
        def wrapper(func):
            thread_new = Thread(target=func, args=[st], daemon=True, name=name)
            thread_new.start()
            Logger.Linelog(f'Запущен поток {name}')
            return func

        return wrapper
