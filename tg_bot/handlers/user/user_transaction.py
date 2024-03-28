from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from tg_bot.database.transactions import select_user, users_transactions, update_balance
from tg_bot.keyboards.reply import income_expenses, ls_family, back, main_menu
from tg_bot.states.user_tr import UserTransaction

user_router: Router = Router()


@user_router.message(F.text == 'Личные')
async def start_register_transaction(message: types.Message, state: FSMContext):
    if message.text == 'Назад ⬅️':
        await message.answer('Действие отменено', reply_markup=ls_family())
        await state.clear()
    else:
        await message.answer('Выберите Доход/Расход',
                             reply_markup=income_expenses())
        await state.set_state(UserTransaction.type_transaction)


@user_router.message(UserTransaction.type_transaction)
async def register_user_transaction(message: types.Message, state: FSMContext):
    if message.text == 'Назад ⬅️':
        await message.answer('Действие отменено', reply_markup=ls_family())
        await state.clear()
    else:
        db_data = await select_user(message.from_user.id)
        user_name = db_data[0][0]
        await state.update_data(user_id=message.from_user.id,
                                type_transaction=message.text,
                                user_name=user_name)
        await message.answer('Введите сумму полностью.\nПример: 20000 (Двадцать тысяч сум)',
                             reply_markup=back())
        await state.set_state(UserTransaction.quantity)


@user_router.message(UserTransaction.quantity)
async def register_quantity(message: types.Message, state: FSMContext):
    if message.text == 'Назад ⬅️':
        await message.answer('Действие отменено', reply_markup=ls_family())
        await state.clear()
    else:
        await state.update_data(quantity=message.text)
        await message.answer('Введите описание', reply_markup=back())
        await state.set_state(UserTransaction.description)


@user_router.message(UserTransaction.description)
async def register_description(message: types.Message, state:FSMContext):
    if message.text == 'Назад ⬅️':
        await message.answer('Действие отменено', reply_markup=ls_family())
        await state.clear()
    else:
        user_id = message.from_user.id
        await state.update_data(description=message.text)
        state_data = await state.get_data()
        user_name = state_data["user_name"]
        type_transaction = state_data["type_transaction"]
        quantity = int(state_data["quantity"])
        description = state_data["description"]
        await state.clear()
        await message.answer(f'ФИО: {user_name}\n'
                             f'Тип транзакции: {type_transaction}\n'
                             f'Сумма: {quantity}\n'
                             f'Описание: {description}')
        if type_transaction == '➕ Доход':
            type_transaction = 'income'
        else:
            type_transaction = 'expenses'
        await users_transactions(user_id, type_transaction, quantity, description, user_name)
        user_info = await select_user(user_id)
        income = user_info[0][3]
        expenses = user_info[0][2]
        if type_transaction == 'income':
            balance = user_info[0][4] + quantity
            income += quantity
        else:
            balance = user_info[0][4] - quantity
            expenses += quantity
        await update_balance(user_id, balance, expenses, income)
        await message.answer('Операция завершена', reply_markup=main_menu())





