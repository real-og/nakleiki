from aiogram import types
from aiogram.dispatcher import FSMContext

import texts
import sheets
import keyboards as kb
from states import State
from loader import dp


@dp.message_handler(commands=['start'], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer(texts.start_message)
    recommendation_number = await sheets.get_number_recommendation(message.from_user.id)
    await message.answer(texts.enter_your_phone, reply_markup=kb.get_number_recommendation_kb(recommendation_number))
    await state.finish()
    await State.entering_your_number.set()


@dp.message_handler(commands=['help'], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer(texts.help_message)

    


