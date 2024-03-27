from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from tg_bot.database.transactions import select_user
from tg_bot.keyboards.reply import income_expenses, ls_family
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
    else:
        telegram_id: int = message.from_user.id
        type_transaction:str = message.text
        await state.update_data(user_id=telegram_id, type_transaction=type_transaction)
        await state.set_state(FamilyTransaction.quantity)
        await message.answer(f'Введите сумму полностью.\nПример: 20000 (Двадцать тысяч сум)',
                             reply_markup=ReplyKeyboardRemove())


@family_router.message(FamilyTransaction.quantity)
async def register_quantity(message: types.Message, state: FSMContext):
    if message.text == 'Назад ⬅️':
        await message.answer('Действие отменено', reply_markup=ls_family())
    else:
        quantity: str = message.text
        await state.update_data(quantity=quantity)
        await message.answer('Введите описание')
        await state.set_state(FamilyTransaction.description)


@family_router.message(FamilyTransaction.description)
async def description(message: types, state: FSMContext):
    if message.text == 'Назад ⬅️':
        await message.answer('Действие отменено', reply_markup=ls_family())
    else:
        db_data = await select_user(message.from_user.id)
        user_name = db_data[0][0]
        await state.update_data(description=message.text)
        state_data = await state.get_data()
        await state.clear()
        await message.answer(f'ФИО: {user_name}\n'
                             f'ID: {state_data["user_id"]}\n'
                             f'Тип транзакции: {state_data["type_transaction"]}\n'
                             f'Сумма: {state_data["quantity"]}\n'
                             f'Описание: {state_data["description"]}', reply_markup=ls_family())



