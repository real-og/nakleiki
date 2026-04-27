import uuid
import os
import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

import sheets
import texts
import buttons
import side_logic
import config_io
import keyboards as kb
from states import State
from loader import dp, bot


@dp.message_handler(state=State.working_on)
async def send_welcome(message: types.Message, state: FSMContext):
    if message.text in [buttons.completed, buttons.uncompleted]:
        await message.answer(texts.enter_photos_after, reply_markup=ReplyKeyboardRemove())
        await State.entering_photos_after.set()
        await state.update_data(is_completed=message.text)
    else:
        await message.answer(texts.use_buttons, reply_markup=kb.completed_work_kb)


@dp.message_handler(content_types=['any'], state=State.entering_photos_after)
async def handle_photo(message: types.Message, state: FSMContext):
    if message.photo or message.document:
        data = await state.get_data()
        photos_after = data.get('photos_after', [])

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
        photos_after.append(filename)
        await state.update_data(photos_after=photos_after)
    else:
        await message.answer(texts.error_photo)


@dp.message_handler(state=State.entering_comment)
async def send_welcome(message: types.Message, state: FSMContext):
    comment = message.text
    await message.answer(texts.enter_was_solo, reply_markup=kb.yes_no_kb)
    await State.entering_was_working_solo.set()
    await state.update_data(comment=comment)


@dp.message_handler(state=State.entering_was_working_solo)
async def send_welcome(message: types.Message, state: FSMContext):
    if message.text in [buttons.yes, buttons.no]:
        if message.text == buttons.yes:
            data = await state.get_data()
            report = texts.generate_report(data)
            await message.answer(report)
            await side_logic.send_photos_album(message, data.get('photos_before'),texts.photos_before)
            await side_logic.send_photos_album(message, data.get('photos_after'),texts.photos_after)
            await message.answer(texts.enter_finish, reply_markup=kb.send_kb)
            await State.last_check.set()

        elif message.text == buttons.no:
            await message.answer(texts.enter_your_percent, reply_markup=ReplyKeyboardRemove())
            await State.entering_my_percent.set()
        await state.update_data(working_solo=message.text)
    else:
        await message.answer(texts.use_buttons, reply_markup=kb.yes_no_kb)


@dp.message_handler(state=State.entering_my_percent)
async def send_welcome(message: types.Message, state: FSMContext):
    solo_percent = message.text
    await message.answer(texts.enter_coworker)
    await State.adding_coworker.set()
    await state.update_data(solo_percent=solo_percent)


@dp.message_handler(state=State.adding_coworker)
async def send_welcome(message: types.Message, state: FSMContext):
    if message.text == buttons.finish:
        data = await state.get_data()
        report = texts.generate_report(data)
        await message.answer(report)
        await side_logic.send_photos_album(message, data.get('photos_before'),texts.photos_before)
        await side_logic.send_photos_album(message, data.get('photos_after'),texts.photos_after)
        await message.answer(texts.enter_finish, reply_markup=kb.send_kb)
        await State.last_check.set()
    else:
        data = await state.get_data()
        teammates = data.get('teammates', [])
        coworker = message.text
        await message.answer(texts.enter_coworker_percent)
        await State.entering_percent_coworker.set()
        teammates.append(coworker)
        await state.update_data(teammates=teammates)


@dp.message_handler(state=State.entering_percent_coworker)
async def send_welcome(message: types.Message, state: FSMContext):
    data = await state.get_data()
    teammates_percent = data.get('teammates_percent', [])
    coworker_percent = message.text
    await message.answer(texts.enter_coworker_or_exit, reply_markup=kb.finish_kb)
    await State.adding_coworker.set()
    teammates_percent.append(coworker_percent)
    await state.update_data(teammates_percent=teammates_percent)


@dp.message_handler(state=State.last_check)
async def send_welcome(message: types.Message, state: FSMContext):
    if message.text == buttons.send:
        await message.answer(texts.result_saved)
        data = await state.get_data()
        row_data = side_logic.form_list_to_append(message.from_user.id, data)

        report = texts.generate_report(data)
        await bot.send_message(config_io.get_value('CHAT_ID'), report)

        await side_logic.send_photos_album(message, data.get('photos_before'),texts.photos_before, bot)
        await side_logic.send_photos_album(message, data.get('photos_after'), texts.photos_after, bot)

        await sheets.append_row_to_work_notes(row_data)
    else:
        await message.answer(texts.use_buttons, reply_markup=kb.send_kb)


