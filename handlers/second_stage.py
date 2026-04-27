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
import uuid
import os
import asyncio


@dp.message_handler(state=State.working_on)
async def send_welcome(message: types.Message):
    phone_number = message.text
    await message.answer(texts.enter_your_city)
    recommendation_city = await sheets.get_city_recommendation()
    await message.answer(texts.enter_your_city, reply_markup=kb.get_city_recommendation_kb(recommendation_city))
    await State.entering_your_city.set()