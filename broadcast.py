
import config_io
import asyncio

from aiogram import Bot
from aiogram.utils.exceptions import (
    BotBlocked,
    ChatNotFound,
    RetryAfter,
    TelegramAPIError,
    UserDeactivated,
)
TOKEN = config_io.get_value('BOT_TOKEN')

USER_IDS = [6150574145,
353261318,
6643344811,
8507704829,
585332246,
1310777673,
758745450,
7607601188,
483399870,
321339843,
360471902,
1160379813,
7714070882,
1162369243,
8996474505,
453867816]

TEXT = """
Привет, в вид работ отдельно вынесен Автобус(задняя) - задняя часть автобуса

Внося данные по этому виду работ, требуется прикрепить 1, а не 4 фото до и 1, а не 4 фото после.

По вопросам @bot_dealla
"""


async def send_to_user(bot: Bot, user_id: int) -> bool:
    while True:
        try:
            await bot.send_message(
                chat_id=user_id,
                text=TEXT,
                disable_web_page_preview=True,
            )
            return True

        except RetryAfter as error:
            print(f"Лимит Telegram. Ждём {error.timeout} сек.")
            await asyncio.sleep(error.timeout)

        except (BotBlocked, ChatNotFound, UserDeactivated):
            print(f"{user_id}: пользователь недоступен")
            return False

        except TelegramAPIError as error:
            print(f"{user_id}: ошибка — {error}")
            return False


async def main():
    bot = Bot(TOKEN, parse_mode="HTML")

    sent = 0
    failed = 0

    try:
        # dict.fromkeys убирает повторяющиеся ID
        for user_id in dict.fromkeys(USER_IDS):
            if await send_to_user(bot, user_id):
                sent += 1
                print(f"{user_id}: отправлено")
            else:
                failed += 1

            await asyncio.sleep(0.05)

    finally:
        await bot.session.close()

    print(f"\nРассылка завершена")
    print(f"Отправлено: {sent}")
    print(f"Не отправлено: {failed}")


if __name__ == "__main__":
    asyncio.run(main())