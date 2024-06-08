from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from database import check_item
from aiogram.utils.keyboard import ReplyKeyboardBuilder


# 🎮 Меню игр
menu_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🎮 Меню игр🎮')],
    [KeyboardButton(text='🛒Магазин🛒')],
    [KeyboardButton(text='👤 Профиль👤')],
    [KeyboardButton(text='🏆Таблица лидеров 🏆')],
    [KeyboardButton(text='💵Перевод💵')],
    [KeyboardButton(text='📞 Контакты📞')]
], resize_keyboard=True,
    input_field_placeholder='👉 Выберите пункт меню'
)

# 🕹️ Выбор игры
games_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🪨 Камень-Ножницы-Бумага', callback_data='game_1')],
    [InlineKeyboardButton(text='🔫 Русская рулетка', callback_data='game_2')],
    [InlineKeyboardButton(text='🕹️ Слоты', callback_data='game_3')],
], resize_keyboard=True)

# 🪨 Камень, ✂️ Ножницы, 📄 Бумага - Игра
game1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🪨 Камень', callback_data='rock')],
    [InlineKeyboardButton(text='✂️ Ножницы', callback_data='scissors')],
    [InlineKeyboardButton(text='📄 Бумага', callback_data='paper')],
    [InlineKeyboardButton(text='↩️ Назад', callback_data='back')]
], resize_keyboard=True)

# 🔫 Русская рулетка - Игра
game2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔄 Крутить барабан', callback_data='rus_roulette')],
    [InlineKeyboardButton(text='↩️ Назад', callback_data='back')]
], resize_keyboard=True)

game3 = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🕹️ Еще раз🕹️')],
    [KeyboardButton(text='↩️ Назад')]
], resize_keyboard=True)

# ↩️ Назад
back = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='↩️ Назад')]
], resize_keyboard=True)

yes_no_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='✅ Да')],
    [KeyboardButton(text='❌ Нет')]
], resize_keyboard=True)

async def ReplyItem():
    items = await check_item()
    if not items:
        return None
    keyboard = ReplyKeyboardBuilder()
    for i in items:
        keyboard.add(KeyboardButton(text=i[0]))
    return keyboard.adjust(2).as_markup()
