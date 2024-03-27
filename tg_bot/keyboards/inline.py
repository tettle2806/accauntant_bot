from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def accept_cancel():
    builder = InlineKeyboardBuilder()
    builder.button(
        text='да',
        callback_data='yes'
    )
    builder.button(
        text='нет',
        callback_data='no'
    )
    builder.adjust(1)
    return builder.as_markup()