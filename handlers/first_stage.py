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


@dp.message_handler(state=State.entering_your_number)
async def send_welcome(message: types.Message):
    phone_number = message.text
    await message.answer('Готово', reply_markup=ReplyKeyboardRemove())
    recommendation_city = await sheets.get_city_recommendation()
    await message.answer(texts.enter_your_city, reply_markup=kb.get_city_recommendation_kb(recommendation_city))
    await State.entering_your_city.set()


@dp.message_handler(state=State.entering_your_city)
async def send_welcome(message: types.Message):
    city = message.text
    recommendation_type_work = await sheets.get_type_work_recommendation()
    await message.answer(texts.enter_type_work, reply_markup=kb.get_type_work_recommendation_kb(recommendation_type_work))
    await State.entering_type_work.set()

@dp.callback_query_handler(state=State.entering_your_city)
async def send_welcome(callback: types.CallbackQuery, state: FSMContext):
    city = callback.data
    print(city)
    recommendation_type_work = await sheets.get_type_work_recommendation()
    await callback.message.answer(texts.enter_type_work, reply_markup=kb.get_type_work_recommendation_kb(recommendation_type_work))
    await State.entering_type_work.set()


@dp.message_handler(state=State.entering_type_work)
async def send_welcome(message: types.Message):
    type_work = message.text
    recommendation_narrative = await sheets.get_narrative_recommendation()
    await message.answer(texts.enter_narrative, reply_markup=kb.get_narrative_recommendation_kb(recommendation_narrative))
    await State.entering_narrative.set()

@dp.callback_query_handler(state=State.entering_type_work)
async def send_welcome(callback: types.CallbackQuery, state: FSMContext):
    type_work = callback.data
    print(type_work)
    recommendation_narrative = await sheets.get_narrative_recommendation()
    await callback.message.answer(texts.enter_narrative, reply_markup=kb.get_narrative_recommendation_kb(recommendation_narrative))
    await State.entering_narrative.set()


@dp.message_handler(state=State.entering_narrative)
async def send_welcome(message: types.Message):
    narrative = message.text
    recommendation_type_transport = await sheets.get_type_transport_recommendation()
    await message.answer(texts.enter_type_transport, reply_markup=kb.get_type_transport_recommendation_kb(recommendation_type_transport))
    await State.entering_type_transport.set()

@dp.callback_query_handler(state=State.entering_narrative)
async def send_welcome(callback: types.CallbackQuery, state: FSMContext):
    narrative = callback.data
    print(narrative)
    recommendation_type_transport = await sheets.get_type_transport_recommendation()
    await callback.message.answer(texts.enter_type_transport, reply_markup=kb.get_type_transport_recommendation_kb(recommendation_type_transport))
    await State.entering_type_transport.set()


@dp.message_handler(state=State.entering_type_transport)
async def send_welcome(message: types.Message):
    type_transport = message.text
    await message.answer(texts.enter_transport_number)
    await State.entering_transport_number.set()

@dp.callback_query_handler(state=State.entering_type_transport)
async def send_welcome(callback: types.CallbackQuery, state: FSMContext):
    type_transport = callback.data
    print(type_transport)
    await callback.message.answer(texts.enter_transport_number)
    await State.entering_transport_number.set()


@dp.message_handler(state=State.entering_transport_number)
async def send_welcome(message: types.Message):
    transport_number = message.text
    await message.answer(texts.enter_route_number)
    await State.entering_route_number.set()


@dp.message_handler(state=State.entering_route_number)
async def send_welcome(message: types.Message):
    route_number = message.text
    await message.answer(texts.enter_photos_before)
    await State.entering_photos_before.set()


@dp.message_handler(content_types=['any'], state=State.entering_photos_before)
async def handle_photo(message: types.Message):
    if message.photo or message.document:

        if message.photo:
            photo = message.photo[-1]
            filename = f"{uuid.uuid4().hex}.jpg"
            path = 'photos/' + filename
            await photo.download(destination_file=str(path))

        elif message.document:
            doc = message.document
            if not doc.mime_type or not doc.mime_type.startswith("image/"):
                await message.answer(texts.error_photo)
                return
            ext = os.path.splitext(doc.file_name or "")[1] or ".jpg"
            filename = f"{uuid.uuid4().hex}{ext}"
            path = 'photos/' + filename
            await doc.download(destination_file=str(path))

        await message.answer(texts.go_to_work, reply_markup=kb.completed_work_kb)
        await asyncio.sleep(1)
        await State.working_on.set()
        print(filename)
    
    else:
        await message.answer(texts.error_photo)
    

    