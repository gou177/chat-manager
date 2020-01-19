from utils import VKboard
from utils.pluginSystem import EPlugin

plugin = EPlugin('Основа')


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
