import os


from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.types import FSInputFile

from config import admin_ids
from database import *
from games import *
from buttons import *

router = Router()
replay = True


class Bet(StatesGroup):
    next = State()


class Transfer(StatesGroup):
    name = State()
    sum = State()
    text = State()


@router.message(CommandStart())
async def start(message: Message):
    try:
        user_id = message.from_user.id
        username = message.from_user.username
        database = await create_database()
        check_u = await check_user_top(user_id)
        if not database:
            await create_database()
        if check_u[0] == 0:
            await add_message(user_id, username)
            await message.answer("Hello!", reply_markup=menu_markup)
            return
        await message.answer("С возвращением!", reply_markup=menu_markup)
    except Exception as e:
        print(e)


@router.message(F.text == "🏆Таблица лидеров 🏆")
async def tab(message: Message):
    try:
        top_users = await get_top()
        leaderboard_text = 'Таблица лидеров:\n'
        for i, (username, money) in enumerate(top_users, start=1):
            leaderboard_text += f'{i}. 😎@{username} - {money} $\n'
        await message.answer(leaderboard_text)
    except Exception as e:
        await message.answer("❗️ Произошла ошибка при получении данных профиля.")
        print(e)


@router.message(F.text == "🎮 Меню игр🎮")
async def menu(message: Message):
    try:
        await message.answer("Вы в меню:", reply_markup=games_markup)
    except Exception as e:
        print(e)


@router.message(F.text == "👤 Профиль👤")
async def contacts(message: Message):
    try:
        user_id = message.from_user.id
        balance = await get_balance(user_id)
        username = message.from_user.username
        await message.answer("👤 Ваш профиль:")
        await message.answer(f"🔤 Ваше имя: {username}\n"
                             f"💰 Ваш баланс: {balance}\n"
                             f"🆔 Ваш ID: {user_id}")
    except Exception as e:
        await message.answer("❗️ Произошла ошибка при получении данных профиля.")
        print(e)


@router.message(F.text == "💵Перевод💵")
async def trade(message: Message, state: FSMContext):
    try:
        await state.set_state(Transfer.name)
        await message.answer("💵Перевод💵:")
        await message.answer("Введите имя пользователя без '@'")
    except Exception as e:
        print(e)


@router.message(Transfer.name)
async def trade_2(message: Message, state: FSMContext):
    try:
        await state.set_state(Transfer.sum)
        name = message.text
        proverka = await check_username(name)
        if proverka is None:
            await message.answer("Пользователь не найден")
            await state.clear()
            return
        await state.update_data(name=name)
        await message.answer("💵Перевод💵:")
        await message.answer("Сколько перевести?")
    except Exception as e:
        print(e)


@router.message(Transfer.sum)
async def trade_3(message: Message, state: FSMContext):
    try:
        await state.set_state(Transfer.text)
        summa = message.text
        if summa.isdigit() is False:
            await message.answer("Сумма должна быть числом")
            return
        await state.update_data(sum=summa)
        user_id = message.from_user.id
        balance_user = await get_balance(user_id)
        if balance_user < int(summa):
            await message.answer("Недостаточно средств", reply_markup=menu_markup)
            await state.clear()
            return
        await message.answer("Укажите сообщение к переводу до 100 символов:")
    except Exception as e:
        print(e)


@router.message(Transfer.text)
async def trade_4(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        data = await state.get_data()
        Name = data.get("name")
        summa = data.get("sum")
        id_to = await check_user_id(Name)
        id_to = id_to[0]
        text = message.text
        if len(text) > 100:
            await message.answer("Сообщение должно быть меньше 100 символов", reply_markup=menu_markup)
            await state.clear()
            return
        user_balance = await get_balance(user_id)
        user_balance -= int(summa)
        if id_to is None:
            await message.answer("Пользователь не найден")
            await state.clear()
            return
        balance_to = await get_balance(id_to)
        balance_to += int(summa)
        await edit_balance(id_to, balance_to)
        await message.bot.send_message(id_to, f"💵Перевод💵 от @{message.from_user.username}:\n"
                                              f"На сумму: {summa}\n"
                                              f"Сообщение: {text}\n")

        await message.answer("Перевод отправлен!")
        await edit_balance(user_id, user_balance)

        await state.clear()
    except Exception as e:
        print(e)


@router.callback_query(F.data == "game_1")
async def game_1(callback: CallbackQuery):
    try:
        await callback.message.edit_text("Выбирай:", reply_markup=game1)
    except Exception as e:
        print(e)


@router.callback_query(F.data == "rock")
async def game_1_1(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        result = await rock_paper_scissors("камень")
        await callback.message.edit_text(result)
        if result == "Победа":
            balance = await get_balance(user_id)
            balance += 100
            await edit_balance(user_id, balance)
            await callback.message.answer(str(+100), reply_markup=game1)
        elif result == "Поражение":
            balance = await get_balance(user_id)
            if balance < 100:
                balance = 0
                await edit_balance(user_id, balance)
        else:
            await callback.message.answer("Ваш баланс не изменился", reply_markup=game1)
    except Exception as e:
        print(e)


@router.callback_query(F.data == "paper")
async def game_1_2(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        result = await rock_paper_scissors("бумага")
        await callback.message.edit_text(result)
        if result == "Победа":
            balance = await get_balance(user_id)
            balance += 100
            await edit_balance(user_id, balance)
            await callback.message.answer(str(+100), reply_markup=game1)
        elif result == "Поражение":
            balance = await get_balance(user_id)
            if balance < 100:
                balance = 0
                await edit_balance(user_id, balance)
        else:
            await callback.message.answer("Ваш баланс не изменился", reply_markup=game1)
    except Exception as e:
        print(e)


@router.callback_query(F.data == "scissors")
async def game_1_3(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        result = await rock_paper_scissors("ножницы")
        await callback.message.edit_text(result)
        if result == "Победа":
            balance = await get_balance(user_id)
            balance += 100
            await edit_balance(user_id, balance)
            await callback.message.answer(str(+100), reply_markup=game1)
        elif result == "Поражение":
            balance = await get_balance(user_id)
            if balance < 100:
                balance = 0
                await edit_balance(user_id, balance)
        else:
            await callback.message.answer("Ваш баланс не изменился", reply_markup=game1)
    except Exception as e:
        print(e)


@router.callback_query(F.data == "game_2")
async def game_2(callback: CallbackQuery):
    try:
        await callback.message.edit_text("Выбирай:", reply_markup=game2)
    except Exception as e:
        print(e)


@router.callback_query(F.data == "rus_roulette")
async def game_2_1(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        balance = await get_balance(user_id)
        if balance <= 0:
            await callback.message.edit_text("Недостаточно средств", reply_markup=games_markup)
            return
        user_choice = random.randint(0, 7)
        result = await russian_roulette(user_choice)
        await callback.message.edit_text(result)
        if result == "Победа":
            balance = balance * 2
            await edit_balance(user_id, balance)
            await callback.message.answer("Ваш баланс увеличился в 2 раза", reply_markup=game2)
        else:
            balance = 0
            await edit_balance(user_id, balance)
            await callback.message.answer("🫡Вы проиграли", reply_markup=game2)
    except Exception as e:
        print(e)


@router.message(F.text == "📞 Контакты📞")
async def contacts(message: Message):
    try:
        await message.answer("🧠 Гений\n"
                             "💼 Плейбой\n"
                             "💵 Миллионер\n"
                             "❤️ Филантроп\n"
                             "🔗 да и просто: [Хозяин](https://t.me/Programist337)",
                             reply_markup=menu_markup,
                             parse_mode='Markdown')
    except Exception as e:
        print(e)
        await message.answer("❗️ Произошла ошибка при попытке редактирования контактов.")


@router.callback_query(F.data == "game_3")
async def game_3(callback: CallbackQuery, state: FSMContext):
    try:
        # Переход в следующее состояние
        await state.set_state(Bet.next)
        await callback.message.answer("😈Ваша ставка:")
    except Exception as e:
        print(e)


@router.message(Bet.next)
async def bet(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        balance = await get_balance(user_id)
        bet_1 = message.text
        if balance < int(bet_1):
            await message.answer("Недостаточно средств")
            return
        if int(bet_1) < 0:
            await message.answer("Ставка не может быть отрицательной")
            return
        balance -= int(bet_1)
        await edit_balance(user_id, balance)
        answer, rate = await slot_machine()
        await message.answer(f'{str(rate[0])}, {str(rate[1])}, {str(rate[2])}')
        if answer == "Поражение":
            await message.answer("Вы проиграли", reply_markup=game3)
        else:
            await message.answer("Вы выиграли", reply_markup=game3)
            balance = balance * int(answer)
            await edit_balance(user_id, balance)
        await state.clear()
    except Exception as e:
        print(e)


@router.message(F.text == "🕹️ Еще раз🕹️")
async def game_3_1(message: Message, state: FSMContext):
    try:
        await state.set_state(Bet.next)
        await message.answer("😈Ваша ставка:")
    except Exception as e:
        print(e)


@router.callback_query(F.data == "back")
async def back(callback: CallbackQuery):
    try:
        await callback.message.answer("Вы в меню:")
    except Exception as e:
        print(e)


@router.message(F.text == "↩️ Назад")
async def back_Reply(message: Message):
    try:
        await message.answer("Вы в меню:", reply_markup=menu_markup)
    except Exception as e:
        print(e)


@router.message(Command('base'))
async def base(message: Message):
    try:
        user_id = message.from_user.id
        print(user_id, admin_ids)
        if str(user_id) not in admin_ids:
            await message.answer("Только для админов")
            return
        await message.answer("Отправляю базу данных")
        if os.path.exists("user_database.db"):
            await message.answer_document(FSInputFile("user_database.db"))
        else:
            await message.answer("База данных нет")

    except Exception as e:
        print(e)
