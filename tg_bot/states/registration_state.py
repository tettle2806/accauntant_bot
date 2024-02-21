from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    telegram_id = State()
    name = State()
    phone = State()


