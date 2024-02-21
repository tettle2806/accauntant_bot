from aiogram import Bot, Dispatcher

from tg_bot.data.config import token
from aiogram.fsm.storage.memory import MemoryStorage


storage = MemoryStorage()

bot = Bot(token=token)
dp = Dispatcher(storage=storage)

