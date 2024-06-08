from aiogram.fsm.state import State, StatesGroup

class Bet(StatesGroup):
    next = State()


class Transfer(StatesGroup):
    name = State()
    sum = State()
    text = State()


class Edit(StatesGroup):
    username = State()
    money = State()


class Shop(StatesGroup):
    object = State()
    price = State()
    about = State()


class Buy(StatesGroup):
    object = State()
    price = State()

class Delete(StatesGroup):
    name = State()