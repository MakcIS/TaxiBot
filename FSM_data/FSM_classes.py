from aiogram.fsm.state import State, StatesGroup


class FSMOrderTaxiProcess(StatesGroup):
    from_input = State()
    to_input = State()
    check_order_data = State()

class FSMOrderFoodProcess(StatesGroup):
    shopping_list = State()
    to_input = State()
