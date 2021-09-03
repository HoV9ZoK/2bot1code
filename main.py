from src import *
from asyncio import get_event_loop

loop = get_event_loop()

vk_bot = VkBot('vk bot token', 1234567890)
tg_bot = TelegramBot('tg bot token', loop)

register_echo_handler(vk_bot)
register_echo_handler(tg_bot)


if __name__ == '__main__':
    vk_bot.run_forever(loop=loop)
    # ТГ запускается после т.к. в коде aiogram'а хрен уберешь loop.run_forever()
    tg_bot.run_forever()
