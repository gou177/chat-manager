from utils import EPlugin
from enum import Enum

plugin = EPlugin(theme='command')

class Test(Enum):
    list_admin = [423904265]
    balance = 0

@plugin.on_command(['кик'])
def kick(args, store):
    store.send(f'Вы кикнули человека')


@plugin.on_command(['id'])
def id_user(args, store):
    store.send(f'Ваш id: {store.user_id}')

@plugin.on_command(['проверка'])
def test(args, store):
    store.send(f'{args}')

@plugin.on_command(['admin'])
def admin(args, store):
    if store.user_id in Test.list_admin.value:
        store.send('Типо только админы сюда попасть могут')
    else:
        store.send('Ты не админ хех')

@plugin.on_command(['добавить'])
def klicker(args, store):
    if store.user_id in Test.list_admin.value:
        if args[0] not in Test.list_admin.value:
            Test.list_admin.value.append(args[0])
            print('Успешно')
        else:
            store.send('Типо пользователь есть уже')
    else:
        store.send('ТЫ НЕ АДМИН')

