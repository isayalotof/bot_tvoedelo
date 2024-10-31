from aiogram.fsm.state import StatesGroup, State


class Recording(StatesGroup):
    userid = State()
    category = State()
    serves_name = State()
    rec_data = State()
    time_start = State()
    duration = State()
    comment = State()








