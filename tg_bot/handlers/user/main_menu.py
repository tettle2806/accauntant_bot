from aiogram import Router, types, F

from tg_bot.data.config import type_of_review, admin_id
from tg_bot.database.transactions import select_user, get_family_by_id
from tg_bot.keyboards.reply import ls_family, main_menu, review

main_router = Router()


@main_router.message(F.text == '✨ Профиль')
async def profile(message: types.Message):
    telegram_id = message.from_user.id
    info = await select_user(telegram_id)
    if info[0][5]:
        families = await get_family_by_id(info[0][5])
        name = families[0][1]
    else:
        families = 'Вы не состоите в семье'
    text = f'''
    ℹ️ ФИО: {info[0][0]}\n
☎️ Телофон: {info[0][1]}\n
➖ Затраты: {info[0][2]}\n
➕ Прибыль: {info[0][3]}\n
💵 Баланс: {info[0][4]}\n
👨🏻‍👩🏻‍🧒🏻 Семья: {name}\n
🕛 Дата регистрации: {info[0][6]}'''

    await message.answer(text)


@main_router.message(F.text == 'Действия')
async def logic(message: types.Message):
    await message.answer('Выберите тип', reply_markup=ls_family())


@main_router.message(F.text == '🔙 Назад')
async def back(message: types.Message):
    await message.answer('Главное меню', reply_markup=main_menu())

@main_router.message(F.text == 'ℹ️ Информация о боте')
async def about(message: types.Message):
    await message.answer('Данный бот разработан https://t.me/LLlARAVOY')


@main_router.message(F.text == '✍ Оставить отзыв')
async def feed_back(message: types.Message):
    await message.answer('Выберите одно', reply_markup=review())


@main_router.message(lambda message: message.text in type_of_review)
async def send_admin(message: types.Message):
    user_id = message.from_user.id
    info_about_user = await select_user(user_id)
    text = f'Имя: {info_about_user[0][0]}\n' \
           f'ID: {user_id}\n' \
           f'Номер телефона: {info_about_user[0][1]}\n' \
           f'Отзыв: {message.text}'

    await message.bot.send_message(chat_id=admin_id, text=text)