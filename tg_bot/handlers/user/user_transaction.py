from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from tg_bot.database.transactions import select_user
from tg_bot.keyboards.reply import income_expenses, ls_family
from tg_bot.states.user_tr import UserTransaction

user_router: Router = Router()


@user_router.message(F.text == 'Личные')
async def start_register_transaction(message: types.Message, state: FSMContext):
    await message.answer('Выберите Доход/Расход',
                         reply_markup=income_expenses())
    await state.set_state(UserTransaction.type_transaction)


@user_router.message(UserTransaction.type_transaction)
async def register_user_transaction(message: types.Message, state: FSMContext):
    db_data = await select_user(message.from_user.id)
    user_name = db_data[0][0]
    await state.update_data(user_id=message.from_user.id,
                            type_transaction=message.text,
                            user_name=user_name)
    await message.answer('Введите сумму полностью.\nПример: 20000 (Двадцать тысяч сум)',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserTransaction.quantity)


@user_router.message(UserTransaction.quantity)
async def register_quantity(message: types.Message, state: FSMContext):
    await state.update_data(quantity=message.text)
    await message.answer('Введите описание')
    await state.set_state(UserTransaction.description)


@user_router.message(UserTransaction.description)
async def register_description(message: types.Message, state:FSMContext):
    await state.update_data(description=message.text)
    state_data = await state.get_data()
    print(state_data)
    await state.clear()
    await message.answer(f'ФИО: {state_data["user_name"]}\n'
                         f'ID: {state_data["user_id"]}\n'
                         f'Тип транзакции: {state_data["type_transaction"]}\n'
                         f'Сумма: {state_data["quantity"]}\n'
                         f'Описание: {state_data["description"]}', reply_markup=ls_family())


