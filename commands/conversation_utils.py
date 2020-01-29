from typing import List

from common.Store import Stoaring
from utils import *
from .marking_db.marking_db import is_user_marked, mark_user, unmark_user, delete_mark

plugin = EPlugin(theme="ConversationUtils")

@plugin.on_command(["summon", "сбор"])
def summon(args: List[str], store: Stoaring):
    if len(args) == 0: 
        result = start_result = "\nОбщий сбор!\n"
    else:
        result = "Общий сбор среди тех, кто "
        if len(args) > 1:
            for i in range(len(args) - 1):
                result += args[i] + ", "
            result += 'и ' + args[len(args) - 1] + "!\n"
        else:
            result += args[0] + "!\n"
        start_result = result
    
    marks = []
    online = False
    for arg in args:
        if arg in ("online", "онлайн"): 
            online = True
        else: 
            marks.append(arg)
    
    members = store.vk.messages.getConversationMembers(peer_id=store.peer_id)['profiles']
    for mem in members:
        user_has_marks = all(
            [is_user_marked(store.peer_id, mark, mem["id"]) for mark in marks]
        )
        if (mem['online'] or not online) and user_has_marks:
            if 'screen_name' not in mem.keys():
                continue # Если человек DELETED
            result += '['+mem['screen_name']+'|'+mem['first_name']+'] '

    if result == start_result: 
        return store.send("По данным аргументам никого не найдено")

    return store.send(result)

@plugin.on_command("mark")
def mark(args: List[str], store: Stoaring):
    if len(args) < 2:
        return store.send(
            "Неправильное использование команды"
            "\n\nИспользование: /mark <id> <отметка>"
        )
    else:
        if args[0].startswith('@'):
            args[0] = args[0][1:]
        vk_id = None
        try:
            vk_id = store.vk.utils.resolveScreenName(screen_name=args[0])["object_id"]
        except KeyError:
            store.send(
                (
                "Неправильный id. Убедитесь, что id - не ссылка, "
                "или попробуйте без @ или *"
                )
            )
            return
        except TypeError:
            store.send(
                (
                "Неправильный id. Убедитесь, что id - не ссылка, "
                "или попробуйте без @ или *"
                )
            )
            return

        print("Отмечаю пользователя id%i в чате %i как %s" % (vk_id, store.peer_id, args[1]))
        mark_user(store.peer_id, args[1], vk_id)

        return store.send("Успешно")

@plugin.on_command("unmark")
def mark(args: List[str], store: Stoaring):
    if len(args) < 2:
        return store.send(
            "Неправильное использование команды"
            "\n\nИспользование: /unmark <id> <отметка>"
        )
    else:
        if args[0].startswith('@'):
            args[0] = args[0][1:]
        vk_id = None
        try:
            vk_id = store.vk.utils.resolveScreenName(screen_name=args[0])["object_id"]
        except KeyError:
            store.send(
                (
                "Неправильный id. Убедитесь, что id - не ссылка, "
                "или попробуйте без @ или *"
                )
            )
            return
        except TypeError:
            store.send(
                (
                "Неправильный id. Убедитесь, что id - не ссылка, "
                "или попробуйте без @ или *"
                )
            )
            return

        result = unmark_user(store.peer_id, args[1], vk_id)
        
        return store.send("Успешно" if result else "Отметка отсутствует")

@plugin.on_command("delmark")
def delmark(args: List[str], store: Stoaring):
    if len(args) == 0:
        return store.send(
            "Неправильное использование команды"
            "\n\nИспользование: /delmark <отметка_1> "
            "[отметка_2 отметка_3 ... отметка_n]"
        )
    else:
        deleted = 0
        not_found = 0
        for mark in args:
            if delete_mark(store.peer_id, mark):
                deleted += 1
            else:
                not_found += 1
        
        return store.send(
            "Операция завершена. Удалено %i "
            "отметок и %i отметок не найдено" % (deleted, not_found)
        )

@plugin.on_command(["69", "420"])
def nice(args: List[str], store: Stoaring):
    return store.send("Nice")