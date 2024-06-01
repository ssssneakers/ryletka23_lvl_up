import random
from config import symbols

async def slot_machine():
    bet = [random.choice(symbols)for _ in range(3)]
    if bet == ["💎", "💎", "💎"]:
        return "10000", bet
    if bet == ["🍀", "🍀", "🍀"]:
        return "1000", bet
    if bet == ["🔔", "🔔", "🔔"]:
        return "100", bet
    if bet == ["🍊", "🍊", "🍊"]:
        return "10", bet
    if bet == ["🍇", "🍇", "🍇"]:
        return "50", bet
    if bet == ["🌟", "🌟", "🌟"]:
        return "500", bet
    if bet == ["🎰", "🎰", "🎰"]:
        return "1000000000", bet
    if bet == ["🍒", "🍒", "🍒"]:
        return "100000", bet
    else:
        return "Поражение", bet

async def rock_paper_scissors(user_answer):
    choice = ["камень", "ножницы", "бумага"]
    bot_choice = random.choice(choice)

    if user_answer == bot_choice:
        return "Ничья"

    if user_answer == "камень":
        if bot_choice == "ножницы":
            return "Победа"
        if bot_choice == "бумага":
            return "Поражение"

    if user_answer == "ножницы":
        if bot_choice == "камень":
            return "Поражение"
        if bot_choice == "бумага":
            return "Победа"

    if user_answer == "бумага":
        if bot_choice == "камень":
            return "Победа"
        if bot_choice == "ножницы":
            return "Поражение"


async def russian_roulette(user_choice):
    bot_choice = random.randint(0, 7)
    if bot_choice == user_choice:
        return "Смерть"
    else:
        return "Победа"
