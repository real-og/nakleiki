from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
import traceback
from states import State
import keyboards as kb
import texts
import datetime
from loader import dp, bot
import config_io
import sheets
import sys


@dp.message_handler(commands=['start'], state="*")
async def send_welcome(message: types.Message):
    await message.answer(texts.start_message)
    recommendation_number = await sheets.get_number_recommendation(message.from_user.id)
    await message.answer(texts.enter_your_phone, reply_markup=kb.get_number_recommendation_kb(recommendation_number))
    await State.entering_your_number.set()
    


