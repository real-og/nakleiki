from aiogram import types
from aiogram.dispatcher import FSMContext

import navigation
import texts
import sheets
import keyboards as kb
from states import State
from loader import dp
from telegram_safe import safe_answer, notify_user_about_error


@dp.message_handler(commands=['start'], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    await safe_answer(message, texts.start_message)

    await state.finish()

    user = await sheets.get_user(message.from_user.id)
    if (user is None) or (not user[2]):
        await safe_answer(message, texts.reg_number)
        await State.reg_number.set()
        await navigation.push_state(state, State.reg_number.state)
        if user is None:
            await sheets.append_row_to_buffer([message.from_user.id, message.from_user.username])
        return
    
    if not user[3]:
        await safe_answer(message, texts.reg_name)
        await State.reg_name.set()
        await navigation.push_state(state, State.reg_name.state)
        return

    await safe_answer(message, texts.enter_begin, reply_markup=kb.begin_kb)
    
    await State.entering_begin.set()
    await navigation.push_state(state, State.entering_begin.state)
    # await State.entering_comment.set()


@dp.message_handler(commands=['help'], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    await safe_answer(message, texts.help_message)


@dp.errors_handler()
async def global_error_handler(update: types.Update, exception: Exception):
    """Last-resort handler for exceptions not handled inside ordinary handlers."""
    import logging

    logging.getLogger(__name__).error(
        "Unhandled exception while processing Telegram update: %r",
        exception,
        exc_info=(type(exception), exception, exception.__traceback__),
    )

    await notify_user_about_error(update)
    return True
