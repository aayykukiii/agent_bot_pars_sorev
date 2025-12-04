from aiogram.fsm.state import State, StatesGroup

class FindState(StatesGroup):
    waiting_language = State()
    waiting_salary = State()
    waiting_format = State()
    waiting_days = State()
