from typing import Dict

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from tg_bot.database.transactions import select_user, family_transactions, get_family, get_family_by_id, \
    update_balance_family
from tg_bot.keyboards.reply import income_expenses, ls_family, main_menu, back
from tg_bot.states.families_tr import FamilyTransaction

family_router: Router = Router()


@family_router.message(F.text == 'Семейные')
async def start_register_transaction(message: types.Message, state: FSMContext):
    telegram_id: int = message.from_user.id
    user_in_family = await select_user(telegram_id)
    if user_in_family[0][5] is None:
        await message.answer('Вы не состоите в семье', reply_markup=ls_family())
        await state.clear()
    else:

        await message.answer('Выберите Доход/Расход', reply_markup=income_expenses())
        await state.set_state(FamilyTransaction.type_transaction)


@family_router.message(FamilyTransaction.type_transaction)
async def register_type_transaction(message: types.Message, state: FSMContext):
    if message.text == 'Назад ⬅️':
        await message.answer('Действие отменено', reply_markup=ls_family())
        await state.clear()

    else:
        telegram_id: int = message.from_user.id
        type_transaction:str = message.text
        await state.update_data(user_id=telegram_id, type_transaction=type_transaction)
        await state.set_state(FamilyTransaction.quantity)
        await message.answer(f'Введите сумму полностью.\nПример: 20000 (Двадцать тысяч сум)',
                             reply_markup=back())


@family_router.message(FamilyTransaction.quantity)
async def register_quantity(message: types.Message, state: FSMContext):
    if message.text == 'Назад ⬅️':
        await message.answer('Действие отменено', reply_markup=ls_family())
        await state.clear()
    else:
        quantity: str = message.text
        await state.update_data(quantity=quantity)
        await message.answer('Введите описание', reply_markup=back())
        await state.set_state(FamilyTransaction.description)


@family_router.message(FamilyTransaction.description)
async def description(message: types, state: FSMContext):
    if message.text == 'Назад ⬅️':
        await message.answer('Действие отменено', reply_markup=ls_family())
        await state.clear()
    else:
        user_id = message.from_user.id
        db_data = await select_user(user_id)
        user_name = db_data[0][0]
        await state.update_data(description=message.text)
        state_data: Dict = await state.get_data()
        type_transaction = state_data["type_transaction"]
        quantity = int(state_data["quantity"])
        description = state_data["description"]
        family_id = db_data[0][5]
        await state.clear()
        await message.answer(f'ФИО: {user_name}\n'
                             f'Тип транзакции: {type_transaction}\n'
                             f'Сумма: {quantity}\n'
                             f'Описание: {description}', reply_markup=ls_family())

        if type_transaction == '➕ Доход':
            type_transaction = 'income'
        else:
            type_transaction = 'expenses'

        await family_transactions(user_id, type_transaction, quantity, description, family_id)
        family_info_db = await get_family_by_id(family_id)
        income = family_info_db[0][4]
        expenses = family_info_db[0][5]
        print('------------------------------')
        print(income)
        print('------------------------------')
        if type_transaction == 'income':
            balance = family_info_db[0][3] + quantity
            income += quantity
        else:
            balance = family_info_db[0][3] - quantity
            expenses += quantity

        await update_balance_family(family_id, income, balance, expenses)
        await message.answer('Операция завершена', reply_markup=main_menu())

