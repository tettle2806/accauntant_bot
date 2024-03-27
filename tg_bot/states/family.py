from aiogram.fsm.state import State, StatesGroup


class FamilyCreate(StatesGroup):
    '''
    Стейты чтобы создать семью
    '''
    family_name = State()
    family_pass = State()


class FamilyStates(StatesGroup):
    '''
    Стейты чтобы войти в семью
    '''
    family_name = State()
    family_pass = State()
