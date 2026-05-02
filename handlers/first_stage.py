import uuid
import os
import asyncio
from collections import defaultdict

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

import sheets
import texts
import buttons
import keyboards as kb
from states import State
from loader import dp

MIN_PASSPORT_PHOTOS = 2
MIN_BEFORE_PHOTOS = 4
MIN_AFTER_PHOTOS = 4

USER_PHOTO_LOCKS = defaultdict(asyncio.Lock)



@dp.message_handler(state=State.entering_begin)
async def send_welcome(message: types.Message, state: FSMContext):
    user_input = message.text
    if not(user_input == buttons.begin):
        await message.answer(texts.use_buttons, reply_markup=kb.begin_kb)
        return
    
    await state.finish()
    recommendation_city = await sheets.get_city_recommendation()
    await message.answer(texts.begin_tapped, reply_markup=ReplyKeyboardRemove())
    await message.answer(texts.enter_your_city, reply_markup=kb.get_city_recommendation_kb(recommendation_city))
    await State.entering_your_city.set()
    user = await sheets.get_user(message.from_user.id)
    await state.update_data(worker_number=user[2])
    await state.update_data(worker_name=user[3])


@dp.message_handler(state=State.entering_your_city)
async def send_welcome(message: types.Message, state: FSMContext):
    city = message.text
    recommendation_type_work = await sheets.get_type_work_recommendation()
    await message.answer(texts.enter_type_work, reply_markup=kb.get_type_work_recommendation_kb(recommendation_type_work))
    await State.entering_type_work.set()
    await state.update_data(city=city)
    

@dp.callback_query_handler(state=State.entering_your_city)
async def send_welcome(callback: types.CallbackQuery, state: FSMContext):
    city = callback.data
    recommendation_type_work = await sheets.get_type_work_recommendation()
    await callback.message.answer(texts.enter_type_work, reply_markup=kb.get_type_work_recommendation_kb(recommendation_type_work))
    await State.entering_type_work.set()
    await state.update_data(city=city)
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)


@dp.message_handler(state=State.entering_type_work)
async def send_welcome(message: types.Message, state: FSMContext):
    type_work = message.text
    recommendation_narrative = await sheets.get_narrative_recommendation()
    text_to_answer = texts.enter_narrative
    if type_work == 'Демонтаж-Монтаж':
        text_to_answer += '<b> демонтажа</b>'
    await message.answer(text_to_answer, reply_markup=kb.get_narrative_recommendation_kb(recommendation_narrative))
    await State.entering_narrative.set()
    await state.update_data(type_work=type_work)

@dp.callback_query_handler(state=State.entering_type_work)
async def send_welcome(callback: types.CallbackQuery, state: FSMContext):
    type_work = callback.data
    recommendation_narrative = await sheets.get_narrative_recommendation()
    text_to_answer = texts.enter_narrative
    if type_work == 'Демонтаж-Монтаж':
        text_to_answer += '<b> демонтажа</b>'
    await callback.message.answer(text_to_answer, reply_markup=kb.get_narrative_recommendation_kb(recommendation_narrative))
    await State.entering_narrative.set()
    await state.update_data(type_work=type_work)
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)


@dp.message_handler(state=State.entering_narrative)
async def send_welcome(message: types.Message, state: FSMContext):
    narrative = message.text
    recommendation_type_transport = await sheets.get_type_transport_recommendation()
    await message.answer(texts.enter_type_transport, reply_markup=kb.get_type_transport_recommendation_kb(recommendation_type_transport))
    await State.entering_type_transport.set()
    await state.update_data(narrative=narrative)

@dp.callback_query_handler(state=State.entering_narrative)
async def send_welcome(callback: types.CallbackQuery, state: FSMContext):
    narrative = callback.data
    recommendation_type_transport = await sheets.get_type_transport_recommendation()
    await callback.message.answer(texts.enter_type_transport, reply_markup=kb.get_type_transport_recommendation_kb(recommendation_type_transport))
    await State.entering_type_transport.set()
    await state.update_data(narrative=narrative)
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)


@dp.message_handler(state=State.entering_type_transport)
async def send_welcome(message: types.Message, state: FSMContext):
    type_transport = message.text
    await message.answer(texts.enter_transport_number)
    await State.entering_transport_number.set()
    await state.update_data(type_transport=type_transport)

@dp.callback_query_handler(state=State.entering_type_transport)
async def send_welcome(callback: types.CallbackQuery, state: FSMContext):
    type_transport = callback.data
    await state.update_data(type_transport=type_transport)
    await callback.message.answer(texts.enter_transport_number)
    await State.entering_transport_number.set()
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)



@dp.message_handler(state=State.entering_transport_number)
async def send_welcome(message: types.Message, state: FSMContext):
    transport_number = message.text

    data = await state.get_data()
    type_transport = data.get('type_transport')
    if type_transport in ['Маршрутка', 'Такси']:
        await message.answer(texts.enter_representative, kb.no_info_kb)
        await State.entering_representative.set()
    else:
        await message.answer(texts.enter_photos_passport, reply_markup=kb.no_info_kb)
        await State.entering_photos_passport.set()
    await state.update_data(transport_number=transport_number)


@dp.message_handler(state=State.entering_representative)
async def send_welcome(message: types.Message, state: FSMContext):
    representative = message.text
    data = await state.get_data()
    type_transport = data.get('type_transport')
    if type_transport == 'Маршрутка':
        await message.answer(texts.enter_route_number)
        await State.entering_route_number.set()
    else:
        await message.answer(texts.enter_photos_passport, reply_markup=kb.no_info_kb)
        await State.entering_photos_passport.set()
    await state.update_data(representative=representative)


@dp.message_handler(state=State.entering_route_number)
async def send_welcome(message: types.Message, state: FSMContext):
    route_number = message.text
    await message.answer(texts.enter_photos_passport, reply_markup=kb.no_info_kb)
    await State.entering_photos_passport.set()
    await state.update_data(route_number=route_number)


@dp.message_handler(content_types=['any'], state=State.entering_photos_passport)
async def handle_photo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    async with USER_PHOTO_LOCKS[user_id]:
        data = await state.get_data()
        photos_passport = data.get('photos_passport', [])
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

            photos_passport.append(filename)
            photos_count = len(photos_passport)
            await state.update_data(photos_passport=photos_passport)
            if photos_count <= MIN_PASSPORT_PHOTOS:
                await message.answer(f"Принято {photos_count}/{MIN_PASSPORT_PHOTOS} фото.")
            if photos_count == MIN_PASSPORT_PHOTOS:
                await message.answer(texts.enter_photos_before)
                await State.entering_photos_before.set()
        else:
            if message.text == buttons.no_info:
                await message.answer(texts.enter_photos_before, reply_markup=ReplyKeyboardRemove())
                await State.entering_photos_before.set()

            await message.answer(texts.error_photo)


@dp.message_handler(content_types=['any'], state=State.entering_photos_before)
async def handle_photo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    async with USER_PHOTO_LOCKS[user_id]:
        data = await state.get_data()
        photos_before = data.get('photos_before', [])
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

            photos_before.append(filename)
            photos_count = len(photos_before)
            await state.update_data(photos_before=photos_before)
            if photos_count <= MIN_BEFORE_PHOTOS:
                await message.answer(f"Принято {photos_count}/{MIN_BEFORE_PHOTOS} фото.")
            if photos_count == MIN_BEFORE_PHOTOS:
                await message.answer(texts.go_to_work, reply_markup=kb.completed_work_kb)
                await State.working_on.set()
        else:
            await message.answer(texts.error_photo)
    

    