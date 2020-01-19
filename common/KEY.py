from vk_api.keyboard import VkKeyboard, VkKeyboardColor, VkKeyboardButton
from vk_api.utils import sjson_dumps

keyboard = VkKeyboard(inline=True)
keyboard.add_button(label='тестовая', color = VkKeyboardColor.POSITIVE, payload="{\"button\": \"1\"}")