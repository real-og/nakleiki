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
import buttons
import side_logic


@dp.message_handler(state=State.working_on)
async def send_welcome(message: types.Message):
    if message.text in [buttons.completed, buttons.uncompleted]:
        print(message.text)
        await message.answer(texts.enter_photos_after, reply_markup=ReplyKeyboardRemove())
        await State.entering_photos_after.set()
    else:
        await message.answer(texts.use_buttons, reply_markup=kb.completed_work_kb)


@dp.message_handler(content_types=['any'], state=State.entering_photos_after)
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

        await message.answer(texts.enter_comment, reply_markup=kb.skip_comment_kb)
        await asyncio.sleep(1)
        await State.entering_comment.set()
        print(filename)
    else:
        await message.answer(texts.error_photo)


@dp.message_handler(state=State.entering_comment)
async def send_welcome(message: types.Message):
    comment = message.text
    await message.answer(texts.enter_was_solo, reply_markup=kb.yes_no_kb)
    await State.entering_was_working_solo.set()


@dp.message_handler(state=State.entering_was_working_solo)
async def send_welcome(message: types.Message, state: FSMContext):
    if message.text in [buttons.yes, buttons.no]:
        print(message.text)
        if message.text == buttons.yes:
            data = await state.get_data()
            report = texts.generate_report(data)
            await message.answer(report)
            await side_logic.send_photos_album(message, data.get('photos_before', texts.photos_before))
            await side_logic.send_photos_album(message, data.get('photos_after', texts.photos_after))
            await message.answer(texts.enter_finish, reply_markup=kb.send_kb)
            await State.last_check.set()
        elif message.text == buttons.no:
            await message.answer(texts.enter_your_percent, reply_markup=ReplyKeyboardRemove())
            await State.entering_my_percent.set()
    else:
        await message.answer(texts.use_buttons, reply_markup=kb.yes_no_kb)


@dp.message_handler(state=State.entering_my_percent)
async def send_welcome(message: types.Message):
    my_percent = message.text
    await message.answer(texts.enter_coworker)
    await State.adding_coworker.set()


@dp.message_handler(state=State.adding_coworker)
async def send_welcome(message: types.Message, state: FSMContext):
    if message.text == buttons.finish:
        data = await state.get_data()
        report = texts.generate_report(data)
        await message.answer(report)
        await side_logic.send_photos_album(message, data.get('photos_before', texts.photos_before))
        await side_logic.send_photos_album(message, data.get('photos_after', texts.photos_after))
        await message.answer(texts.enter_finish, reply_markup=kb.send_kb)
        await State.last_check.set()
    else:
        coworker = message.text
        await message.answer(texts.enter_coworker_percent)
        await State.entering_percent_coworker.set()


@dp.message_handler(state=State.entering_percent_coworker)
async def send_welcome(message: types.Message):
    coworker_percent = message.text
    await message.answer(texts.enter_coworker_or_exit, reply_markup=kb.finish_kb)
    await State.adding_coworker.set()


@dp.message_handler(state=State.last_check)
async def send_welcome(message: types.Message):
    if message.text == buttons.send:
        await message.answer(texts.result_saved)
    else:
        await message.answer(texts.use_buttons, reply_markup=kb.send_kb)


