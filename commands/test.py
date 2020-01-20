from utils import *
import json
plugin = EPlugin(theme='Тест')


@plugin.on_command('test')
def test(args, store):
    return store.send('тест')

