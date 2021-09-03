# import typing
# from aiogram.types.message import Message as TelegramBotEvent
# from src.tg.bot import TelegramBot
# from vkwave.bots.addons.easy.easy_handlers import SimpleBotEvent as VkBotEvent

# Это должна была быть типизация, но я в ней ничего не понимаю. Динамика топ

from src.vk.bot import VkBot


def register_echo_handler(bot):

    @bot.cmd('hi')
    async def echo(event):
        print('Выполняю: ', event)
        await event.answer(f'Hello! Try {"TG" if isinstance(bot, VkBot) else "VK"} too :D')
