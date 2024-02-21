import logging

from aiogram import Bot
import os
from dotenv import load_dotenv
from tg_bot.data.config import admin_id


async def start(bot: Bot):
    try:
        text = 'Бот запущен'
        await bot.send_message(chat_id=admin_id, text=text)
    except Exception as e:
        logging.error(e)
