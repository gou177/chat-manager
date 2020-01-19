import vk_api

import config

session = vk_api.VkApi(token=config.config['group_token'])
api: vk_api.vk_api.VkApiMethod = session.get_api()
upload = vk_api.VkUpload(session)