import asyncio
import logging

import sys

from tg_bot.data.loader import bot, dp
from tg_bot.handlers.admin.bot_started import start
from tg_bot.handlers.user.family_handler import family_hand_router
from tg_bot.handlers.user.family_transaction import family_router
from tg_bot.handlers.user.main_menu import main_router
from tg_bot.handlers.user.registration import registration_router
from tg_bot.handlers.user.user_transaction import user_router


async def main():

    await start(bot)

    dp.include_router(main_router)
    dp.include_router(registration_router)
    dp.include_router(user_router)
    dp.include_router(family_router)
    dp.include_router(family_hand_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exit')
