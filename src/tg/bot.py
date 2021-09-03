from aiogram.bot import Bot as DefaultBot
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_polling


class TelegramBot(Dispatcher):
    """
    Бот с диспетчером с ботом... \n
    Еще и кастомизация отсутствует... \n
    Автора aiogram'а на мыло
    """
    def __init__(self, token: str, loop):
        super().__init__(DefaultBot(token), loop)

    def cmd(self, *args):
        def decorator(func):
            self.register_message_handler(func, commands=args)
        return decorator

    def run_forever(self):
        start_polling(dispatcher=self, loop=self._main_loop)
