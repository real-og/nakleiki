from aiogram import types
from aiogram.dispatcher import FSMContext

import texts
import sheets
import keyboards as kb
from states import State
from loader import dp


@dp.message_handler(commands=['start'], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    print(message)
    await message.answer(texts.start_message)
    await state.finish()
    user = await sheets.get_user(message.from_user.id)

    if (user is None) or (not user[2]):
        await message.answer(texts.reg_number)
        await State.reg_number.set()
        if user is None:
            await sheets.append_row_to_buffer([message.from_user.id, message.from_user.username])
        return
    
    if not user[3]:
        await message.answer(texts.reg_name)
        await State.reg_name.set()
        return

    await message.answer(texts.enter_begin, reply_markup=kb.begin_kb)
    await State.entering_begin.set()
    # await State.entering_comment.set()


@dp.message_handler(commands=['help'], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer(texts.help_message)

    


