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
import sys


@dp.message_handler(commands=['start'], state="*")
async def send_welcome(message: types.Message):
    await message.answer(texts.start_message)
    await message.answer(texts.enter_your_phone)
    await State.entering_yor_number.set()
    