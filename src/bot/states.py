from aiogram.fsm.state import State, StatesGroup

class UploadStates(StatesGroup):
    waiting_for_file = State()
    waiting_for_person = State()