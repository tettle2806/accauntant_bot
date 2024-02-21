from aiogram import types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
import re

from tg_bot.database.transactions import create_user, select_telegram_id_by_phone, select_user
from tg_bot.keyboards.reply import send_phone, main_menu
from tg_bot.states.registration_state import RegistrationStates

registration_router: Router = Router()


@registration_router.message(CommandStart())
async def register_user(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    db_telegram_id = await select_user(telegram_id=telegram_id)
    if db_telegram_id:
        await message.answer('Вы уже зарегестрированы', reply_markup=main_menu())
        await state.clear()
    else:
        await message.answer('Введите ваше ФИО')
        await state.set_state(RegistrationStates.name)


@registration_router.message(RegistrationStates.name)
async def name_user(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer('Отправьте номер телефона', reply_markup=send_phone())
    await state.set_state(RegistrationStates.phone)


@registration_router.message(RegistrationStates.phone)
async def phone_user(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id

    try:
        phone = '+' + message.contact.phone_number
        print(phone)
    except AttributeError as err:
        phone = message.text

    result1 = re.search(r'\+998 \d\d \d\d\d \d\d \d\d', str(phone))
    result2 = re.search(r'\+998\d{9}', str(phone))

    if result1 or result2:
        db_telegram_id = await select_telegram_id_by_phone(phone)
        if db_telegram_id:
            if db_telegram_id == telegram_id:
                await message.answer('Вы уже зарегестрированы', reply_markup=main_menu())
                await state.clear()
            else:
                await message.answer('Этот номер телефона уже зарегестрирован')
                await repeat_phone(message, state)
        else:
            await state.update_data(phone=phone)
            info = await state.get_data()
            name = info['name']
            phone = info['phone']

            await create_user(telegram_id=telegram_id, phone=phone, name=name)
            await state.clear()
            await message.answer(f'Вы зарегестрировались\n'
                                 f'Фио: {name}\n'
                                 f'Номер: {phone}', reply_markup=main_menu())

    else:
        await message.answer('Номер телефона не коректный')
        await repeat_phone(message, state)


async def repeat_phone(message: types.Message, state: FSMContext):
    await state.set_state(RegistrationStates.phone)
    await message.answer('Отправьте номер телефона', reply_markup=send_phone())
