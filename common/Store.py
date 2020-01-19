import datetime
import random
from typing import List

import vk_api

import config
from db import Global
from utils import comma

session = vk_api.VkApi(token=config.config['group_token'])
api: vk_api.vk_api.VkApiMethod = session.get_api()
upload = vk_api.VkUpload(session)


class Stoaring:
    def __init__(self, event):
        self.start_time = datetime.datetime.now()
        self.peer_id = event.obj.peer_id
        self.user_id = event.obj.from_id

        self._alive = True

        self.obj = event.obj
        self.raw = event.raw
        self.event = event
        self._vk = api

        self.body = self.obj.text
        self.upload = upload

    def send(self, text='', attachment=None, sticker_id=None, keyboard=None, reply_to=None, peer_id=None, disable_mentions=1):
        try:
            self._vk.messages.send(
                peer_id=self.peer_id if not peer_id else peer_id,
                message=self.prefix + str(text),
                keyboard=keyboard,
                random_id=self._random,
                attachment=attachment,
                sticker_id=sticker_id,
                disable_mentions=disable_mentions
            )
            self.prefix = ''
        except Exception as s:
            print(s)

    @property
    def _random(self):
        return random.randint(-1000000, 1000000)

    def save(self):
        return self.data.save()

    def update(self, d=None):
        if d:
            self.data: Global = d
            self.prefix = f'@id{self.user_id}({self.data.prefix}), '
        else:
            self.data: Global = Global.select().where(Global.user_id == self.user_id)[0]
            self.prefix = f'@id{self.user_id}({self.data.prefix}), '

    def set_photo(self, p):
        photo = self.upload.photo_messages(p)
        return f'photo{photo[0]["owner_id"]}_{photo[0]["id"]}'

    @property
    def balance(self):
        return comma(self.data.money)

    @property
    def alive(self):
        return self._alive

    def init(self):
        check_db: List[Global] = list(Global.select().where(Global.user_id == self.user_id))
        if check_db:
            if check_db[0].ban:
                self._alive = False
        else:
            get_user = self._vk.users.get(user_id=self.user_id)
            name = get_user[0]["first_name"] + " " + get_user[0]['last_name']
            Global.create(
                user_id=self.user_id,
                prefix=name,
            )
            self.send(f'Жопа')
        self.update()
        return self

    def __repr__(self):
        return f'ctx: {self.user_id}'