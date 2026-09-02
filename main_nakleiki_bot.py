from loader import dp
from aiogram import executor
from handlers import *

async def on_startup(dispatcher):
    me = await dispatcher.bot.get_me()
    print(f"Bot started: @{me.username}", flush=True)


if __name__ == "__main__":
    executor.start_polling(
        dp,
        on_startup=on_startup,
        skip_updates=True,
    )