from aiogram.fsm.state import State, StatesGroup


class FamilyTransaction(StatesGroup):
    user_id = State()
    type_transaction = State()
    quantity = State()
    description = State()
    family_id = State()

