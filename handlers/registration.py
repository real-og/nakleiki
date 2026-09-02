import uuid
import os
import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove


import navigation
import sheets
import texts
import side_logic
import keyboards as kb
from states import State
from loader import dp


@dp.message_handler(state=State.reg_number)
async def send_welcome(message: types.Message, state: FSMContext):
    phone_number = message.text
    if not side_logic.normalize_phone(phone_number):
        await message.answer(texts.bad_number)
        return
    await message.answer(texts.reg_name)
    await State.reg_name.set()
    await navigation.push_state(state, State.reg_name.state)
    await sheets.update_cell_buffer(message.from_user.id, 3, phone_number)


@dp.message_handler(state=State.reg_name)
async def send_welcome(message: types.Message, state: FSMContext):
    name = message.text
    await message.answer(texts.enter_begin, reply_markup=kb.begin_kb)
    await State.entering_begin.set()
    await navigation.push_state(state, State.entering_begin.state)
    await sheets.update_cell_buffer(message.from_user.id, 4, name)
    


    