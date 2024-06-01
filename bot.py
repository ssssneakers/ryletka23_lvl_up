import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import router

dp = Dispatcher()
bot = Bot(BOT_TOKEN)


async def main():
    try:
        dp.include_router(router)
        await dp.start_polling(bot)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError or KeyboardInterrupt:
        print('exit')
