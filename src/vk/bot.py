import asyncio
import typing
from vkwave.bots.addons.easy.easy_handlers import SimpleBotCallback
from vkwave.longpoll import BotLongpoll, BotLongpollData
from vkwave.bots.addons.easy.base_easy_bot import create_api_session_aiohttp
from vkwave.types.bot_events import BotEventType
from vkwave.api import APIOptionsRequestContext
from vkwave.bots import (
    BotLongpollExtension,
    BotType,
    CommandsFilter,
    DefaultRouter,
    Dispatcher,
    EventTypeFilter,
    GroupId,
    TokenStorage,
)


class VkBot:
    """
    Урезанная до эхо бота копия BaseSimpleLongPollBot
    """

    def __init__(
            self,
            tokens: typing.Union[str, typing.List[str]],
            group_id: typing.Optional[int],
    ):

        self.group_id = group_id
        self.api_session = create_api_session_aiohttp(tokens, BotType.BOT)
        self.api_context: APIOptionsRequestContext = self.api_session.api.get_context()
        self._lp = BotLongpoll(self.api_context, BotLongpollData(group_id))
        self._token_storage = TokenStorage[GroupId]()
        self.dispatcher = Dispatcher(self.api_session.api, self._token_storage)
        self._lp = BotLongpollExtension(self.dispatcher, self._lp)

        self.router = DefaultRouter()
        self.dispatcher.add_router(self.router)
        self.command_filter = CommandsFilter

    def cmd(self, *args):
        def decorator(func):
            record = self.router.registrar.new()
            record.filters += [EventTypeFilter(BotEventType.MESSAGE_NEW), CommandsFilter(args)]
            record.handle(SimpleBotCallback(func, BotType.BOT))
            self.router.registrar.register(record.ready())
        return decorator

    async def run(self, ignore_errors: bool = True):
        await self.dispatcher.cache_potential_tokens()
        await self._lp.start(ignore_errors)

    def run_forever(
            self, ignore_errors: bool = True,
            loop: typing.Optional[asyncio.AbstractEventLoop] = None
    ):
        loop = loop or asyncio.get_event_loop()
        loop.create_task(self.run(ignore_errors))
        # loop.run_forever() нам это здесь не надо
