from aiogram import types, Router, F

from tg_bot.database.transactions import select_user
from tg_bot.keyboards.reply import family, un_family

family_hand_router: Router = Router()


@family_hand_router.message(F.text == '👨🏻‍👩🏻‍👧🏻‍👦🏻 Cемья')
async def family_handler(message: types.Message):
    db_info = await select_user(message.from_user.id)
    if db_info[0][5]:
        await message.answer('Выберите действие', reply_markup=family())
    else:
        await message.answer('Выберите действие', reply_markup=un_family())
