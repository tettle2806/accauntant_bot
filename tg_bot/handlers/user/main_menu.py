from aiogram import Router, types, F


from tg_bot.database.transactions import select_user
from tg_bot.keyboards.reply import ls_family, main_menu

main_router = Router()


@main_router.message(F.text == '✨ Профиль')
async def profile(message: types.Message):
    telegram_id = message.from_user.id
    info = await select_user(telegram_id)
    if info[0][5]:
        families = info[0][5]
    else:
        families = 'Вы не состоите в семье'
    text = f'''
    ℹ️ ФИО: {info[0][0]}\n
☎️ Телофон: {info[0][1]}\n
➖ Затраты: {info[0][2]}\n
➕ Прибыль: {info[0][3]}\n
💵 Баланс: {info[0][4]}\n
👨🏻‍👩🏻‍🧒🏻 Семья: {families}\n
🕛 Дата регистрации: {info[0][6]}'''

    await message.answer(text)


@main_router.message(F.text == 'Действия')
async def logic(message: types.Message):
    await message.answer('Выберите тип', reply_markup=ls_family())


@main_router.message(F.text == '🔙 Назад')
async def back(message: types.Message):
    await message.answer('Главное меню', reply_markup=main_menu())