from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton


def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text='✨ Профиль'),
            KeyboardButton(text='👨🏻‍👩🏻‍👧🏻‍👦🏻 Cемья'),
        ],
        [
            KeyboardButton(text='Действия')
        ],
        [
            KeyboardButton(text='⚙️ Настройки'),
            KeyboardButton(text='ℹ️ Информация о боте')
        ]
    ], row_width=2)
    return markup


def send_phone():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text='Номер', request_contact=True)]
    ], row_width=2)
    return markup


def ls_family():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text='Личные'),
            KeyboardButton(text='Семейные')
        ],
        [
            KeyboardButton(text='🔙 Назад')
        ]
    ], row_width=2)
    return markup


def income_expenses():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text='➕ Доход'),
            KeyboardButton(text='➖ Расход')
        ],
        [
            KeyboardButton(text='Назад ⬅️')
        ]
    ], row_width=2)
    return markup


def family():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text='Участники'),
            # KeyboardButton(text='Управление')
            KeyboardButton(text='Информация')
        ],
        [
            KeyboardButton(text='Главное меню')
        ],
        [
            KeyboardButton(text='Выйти из семьи')
        ]
    ], row_width=2)
    return markup


def un_family():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text='Создать семью')
        ],
        [
            KeyboardButton(text='Присоединится к семье')
        ],
        [
            KeyboardButton(text='Назад ⬅️')
        ]
    ], row_width=2)
    return markup

def back():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
                KeyboardButton(text='Назад ⬅️')
        ]
    ], row_width=2)
    return markup
