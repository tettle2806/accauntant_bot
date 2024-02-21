from aiogram.fsm.state import State, StatesGroup


class UserTransaction(StatesGroup):
    user_id = State()
    type_transaction = State()
    quantity = State()
    description = State()
    user_name = State()

