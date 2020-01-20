from utils import VKboard
from utils.pluginSystem import EPlugin
import json

plugin = EPlugin('Основа')


@plugin.on_command('убрать')
def reset_keyboard(args, store):
    return store.send("Убрал!", keyboard=json.dumps({"buttons": [], "one_time": True}))

@plugin.on_command('действия', {'command': 'getActions'})
def getActions(args, store):
    board = VKboard(inline=True)
    board.row()

    row = board.edit(0)
    row.button('Тест 1', {'command': 'test'}, 'positive')
    row.button('тест 2', {'command': 'test2'})

    return store.send('Действия:', keyboard=board.get)


@plugin.on_command(payload={'command': 'test'})
def getActions(args, store):
    return store.send('Первый тест')


@plugin.on_command(payload={'command': 'test2'})
def getActions(args, store):
    return store.send('Второй тест')
