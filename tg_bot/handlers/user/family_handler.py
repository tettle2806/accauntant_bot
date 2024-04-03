from aiogram import types, Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from tg_bot.database.transactions import select_user, get_family, insert_family, update_user, get_family_by_id
from tg_bot.keyboards.inline import accept_cancel
from tg_bot.keyboards.reply import family, un_family, back, main_menu
from tg_bot.states.family import FamilyCreate, FamilyStates

family_hand_router: Router = Router()


@family_hand_router.message(F.text == '👨🏻‍👩🏻‍👧🏻‍👦🏻 Cемья')
async def family_handler(message: types.Message):
    db_info = await select_user(message.from_user.id)
    print(db_info[0][5])
    if db_info[0][5]:
        await message.answer('Выберите действие', reply_markup=family())
    else:
        await message.answer('Выберите действие', reply_markup=un_family())


@family_hand_router.message(F.text == 'Создать семью')
async def create_family(message: types.Message, state: FSMContext):
    await message.answer('Введите название семьи', reply_markup=back())
    await state.set_state(FamilyCreate.family_name)


@family_hand_router.message(FamilyCreate.family_name)
async def save_name_of_family(message: types.Message, state:FSMContext):
    if message.text == 'Назад ⬅️':
        await message.answer('Регистрация отменена', reply_markup=main_menu())
        await state.clear()
    else:
        family_db = await get_family(message.text)
        if family_db is None:
            await message.answer('Введите пароль семьи')
            await state.update_data(name=message.text)
            await state.set_state(FamilyCreate.family_pass)
        else:
            await message.answer('Имя занято, введите другое имя')
            await state.set_state(FamilyCreate.family_name)


@family_hand_router.message(FamilyCreate.family_pass)
async def save_password_of_family(message: types.Message, state:FSMContext):
    if message.text == 'Назад ⬅️':
        await message.answer('Регистрация отменена', reply_markup=main_menu())
        await state.clear()
    else:
        await state.update_data(password=message.text)
        information = await state.get_data()
        family_name = information["name"]
        family_password = information["password"]
        await insert_family(family_name, family_password)
        await state.clear()
        db_info = await get_family(family_name)
        await update_user(message.from_user.id, db_info[0][0])
        await message.answer(f'Регистрация завершена\n'
                             f'Название семьи: {family_name}\n'
                             f'Пароль семьи: {family_password}\n',
                             reply_markup=family())


@family_hand_router.message(F.text=='Назад ⬅️')
async def back_and_finish(message: types.Message, state:FSMContext):
    await state.clear()
    await message.answer('Регистрация отменена',reply_markup=main_menu())

@family_hand_router.message(F.text=='Выйти из семьи')
async def disconnect_family(message: types.Message):
    await message.answer('Вы хотите покинуть семью',reply_markup=accept_cancel())

@family_hand_router.callback_query(F.data == 'yes')
async def accept(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Вы вышли из семьи', reply_markup=main_menu())
    await update_user(callback.from_user.id, None)

@family_hand_router.callback_query(F.data == 'no')
async def cancel(callback: types.CallbackQuery):
    await callback.message.delete()


@family_hand_router.message(F.text == 'Присоединится к семье')
async def connect_family(message: types.Message, state:FSMContext):
    await message.answer('Введите имя семьи', reply_markup=back())
    await state.set_state(FamilyStates.family_name)


@family_hand_router.message(FamilyStates.family_name)
async def connect_to_family(message: types.Message, state:FSMContext):
    if message.text == 'Назад ⬅️':
        await message.answer('Регистрация отменена', reply_markup=main_menu())
        await state.clear()
    else:
        db_info = await get_family(message.text)
        if db_info is None:
            await message.answer('Несуществующая семья, введите название', reply_markup=back())
            await state.set_state(FamilyStates.family_name)
        else:
            await state.update_data(family_name=message.text)
            await message.answer('Введите пароль', reply_markup=back())
            await state.set_state(FamilyStates.family_pass)

@family_hand_router.message(FamilyStates.family_pass)
async def save_password(message: types.Message, state:FSMContext):
    if message.text == 'Назад ⬅️':
        await message.answer('Регистрация отменена', reply_markup=main_menu())
        await state.clear()
    else:
        await state.update_data(password=message.text)
        state_info = await state.get_data()
        db_info = await get_family(state_info['family_name'])
        family_name_db = db_info[0][1]
        family_password_db = db_info[0][2]
        if family_name_db == state_info['family_name'] and family_password_db == state_info['password']:
            await update_user(message.from_user.id, db_info[0][0])
            await message.answer(f'Вы присоединились к семье <b>{family_name_db}</b>',
                                 parse_mode=ParseMode.HTML,
                                 reply_markup=family())
            await state.clear()
        else:
            await message.answer('Не верный пароль, введите еще раз', reply_markup=back())
            await state.set_state(FamilyStates.family_pass)


@family_hand_router.message(F.text == 'Главное меню')
async def back_to_menu(message:types.Message):
    await message.answer('Главное меню', reply_markup=main_menu())


@family_hand_router.message(F.text == 'Информация')
async def information_family(message:types.Message):
    user_id = message.from_user.id
    user_info = await select_user(user_id)
    if user_info is None:
        await message.answer('Вы не зарегистрированы')
    else:
        info = await get_family_by_id(user_info[0][5])

    family_name = info[0][1]
    family_password = info[0][2]
    family_balance = info[0][3]
    family_income = info[0][4]
    family_expenses = info[0][5]
    await message.answer(f'Имя семьи: {family_name}\n'
                         f'Пароль: {family_password}\n'
                         f'Баланс: {family_balance}\n'
                         f'Доходы: {family_income}\n'
                         f'Расходы: {family_expenses}')


