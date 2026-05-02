import uuid
import os
import asyncio
from datetime  import datetime
from collections import defaultdict

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

MIN_AFTER_PHOTOS = 4

USER_PHOTO_LOCKS = defaultdict(asyncio.Lock)


@dp.message_handler(state=State.working_on)
async def send_welcome(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text in [buttons.completed, buttons.uncompleted]:
        if data.get('type_work') == 'Демонтаж-Монтаж':
            await message.answer(texts.enter_photos_after_demontage, reply_markup=ReplyKeyboardRemove())
        else:
            text = f"<i>{data.get('type_work')}\n\n</i>" + texts.enter_photos_after
            await message.answer(text, reply_markup=ReplyKeyboardRemove())
        await State.entering_photos_after.set()
        await state.update_data(is_completed=message.text)
    else:
        await message.answer(texts.use_buttons, reply_markup=kb.completed_work_kb)


@dp.message_handler(content_types=['any'], state=State.entering_photos_after)
async def handle_photo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    async with USER_PHOTO_LOCKS[user_id]:
        data = await state.get_data()
        photos_after = data.get('photos_after', [])
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

            photos_after.append(filename)
            photos_count = len(photos_after)
            await state.update_data(photos_after=photos_after)
            if photos_count <= MIN_AFTER_PHOTOS:
                await message.answer(f"Принято {photos_count}/{MIN_AFTER_PHOTOS} фото.")
            if photos_count == MIN_AFTER_PHOTOS:
                if data.get('type_work') == 'Демонтаж-Монтаж':
                    await message.answer(texts.enter_comment_demontage, reply_markup=kb.skip_comment_kb)
                else:
                    await message.answer(texts.enter_comment, reply_markup=kb.skip_comment_kb)
                await State.entering_comment.set()
                await state.update_data(end_date=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        else:
            await message.answer(texts.error_photo)


@dp.message_handler(state=State.entering_comment)
async def send_welcome(message: types.Message, state: FSMContext):
    data = await state.get_data()
    comment = message.text
    if data.get('type_work') == 'Демонтаж-Монтаж':
        await message.answer(texts.enter_was_solo_demontage, reply_markup=kb.yes_no_kb)
    else:
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
            if data.get('photos_passport'):
                await side_logic.send_photos_album(message, data.get('photos_passport'),texts.photos_passport)
            await side_logic.send_photos_album(message, data.get('photos_before'),texts.photos_before)
            await side_logic.send_photos_album(message, data.get('photos_after'),texts.photos_after)
            if data.get('type_work') == 'Демонтаж-Монтаж':
                await message.answer(texts.enter_finish_demontage, reply_markup=kb.send_kb)
            else:
                await message.answer(texts.enter_finish, reply_markup=kb.send_kb)

            await State.last_check.set()

        elif message.text == buttons.no:
            await message.answer(texts.enter_your_percent, reply_markup=kb.get_percent_kb())
            await State.entering_my_percent.set()
        await state.update_data(working_solo=message.text)
    else:
        await message.answer(texts.use_buttons, reply_markup=kb.yes_no_kb)


# @dp.message_handler(state=State.entering_my_percent)
# async def send_welcome(message: types.Message, state: FSMContext):
#     solo_percent = message.text
#     if side_logic.is_int_0_100(solo_percent):
#         users = await sheets.get_users()
#         data = await state.get_data()
#         if data.get('type_work') == 'Демонтаж-Монтаж':
#             await message.answer(texts.enter_coworker_demontage, reply_markup=kb.get_users_to_select(users))
#         else:
#             await message.answer(texts.enter_coworker, reply_markup=kb.get_users_to_select(users))
#         await State.adding_coworker.set()
#         await state.update_data(solo_percent=solo_percent)
#     else:
#         await message.answer(texts.bad_percent)

@dp.callback_query_handler(state=State.entering_my_percent)
async def send_welcome(callback: types.CallbackQuery, state: FSMContext):
    solo_percent = callback.data
    if side_logic.is_int_0_100(solo_percent):
        users = await sheets.get_users()
        data = await state.get_data()

        if data.get('type_work') == 'Демонтаж-Монтаж':
            await callback.message.answer(
                texts.enter_coworker_demontage,
                reply_markup=kb.get_users_to_select(users)
            )
        else:
            await callback.message.answer(
                texts.enter_coworker,
                reply_markup=kb.get_users_to_select(users)
            )

        await State.adding_coworker.set()
        await state.update_data(solo_percent=solo_percent)

    else:
        await callback.message.answer(texts.bad_percent)
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)




@dp.callback_query_handler(state=State.adding_coworker)
async def send_welcome(callback: types.CallbackQuery, state: FSMContext):
    coworker = callback.data
    data = await state.get_data()

    solo_percent = int(data.get('solo_percent', 0))
    teammate_percent = 100 - int(solo_percent)
    await callback.message.answer(texts.coworker_percent + f'<b>{teammate_percent}</b>')

    teammates = data.get('teammates', [])
    teammates_percent = data.get('teammates_percent', [])
    teammates.append(coworker)
    teammates_percent.append(teammate_percent)
    await state.update_data(teammates_percent=teammates_percent)
    await state.update_data(teammates=teammates)

    data = await state.get_data()

    report = texts.generate_report(data)
    await callback.message.answer(report)
    if data.get('photos_passport'):
        await side_logic.send_photos_album(callback.message, data.get('photos_passport'),texts.photos_passport)
    await side_logic.send_photos_album(callback.message, data.get('photos_before'),texts.photos_before)
    await side_logic.send_photos_album(callback.message, data.get('photos_after'),texts.photos_after)
    if data.get('type_work') == 'Демонтаж-Монтаж':
        await callback.message.answer(texts.enter_finish_demontage, reply_markup=kb.send_kb)
    else:
        await callback.message.answer(texts.enter_finish, reply_markup=kb.send_kb)

    await State.last_check.set()
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)


@dp.message_handler(state=State.last_check)
async def send_welcome(message: types.Message, state: FSMContext):
    if message.text == buttons.send:
        data = await state.get_data()
        await message.answer("Отправляем, немного подождите")

        report = texts.generate_report(data)
        await bot.send_message(config_io.get_value('CHAT_ID'), report)
        if data.get('photos_passport'):
            await side_logic.send_photos_album(message, data.get('photos_passport'),texts.photos_passport, bot)
        await side_logic.send_photos_album(message, data.get('photos_before'),texts.photos_before, bot)
        await side_logic.send_photos_album(message, data.get('photos_after'), texts.photos_after, bot)

        row_data = side_logic.form_list_to_append(message.from_user.id, data)
        await sheets.append_row_to_work_notes(row_data)
        # side_logic.delete_files_from_folder(data.get('photos_passport', []), 'photos')
        # side_logic.delete_files_from_folder(data.get('photos_before', []), 'photos')
        # side_logic.delete_files_from_folder(data.get('photos_after', []), 'photos')
        if data.get('type_work') == 'Демонтаж-Монтаж':
            recommendation_narrative = await sheets.get_narrative_recommendation()
            await message.answer(texts.result_saved_demontage, reply_markup=kb.get_narrative_recommendation_kb(recommendation_narrative))
            await side_logic.remake_data_after_demontage(state)
            await State.entering_narrative.set()
        else:
            await message.answer(texts.result_saved, reply_markup=kb.begin_kb)
            await State.entering_begin.set()
    elif message.text == buttons.reset:
        await message.answer("Данные по этой работе сброшены")
        await state.finish()
        await State.entering_begin.set()
        await message.answer("Можете приступать к следующей работе. Нажимайте или вводите <b>Приступить</b>", reply_markup=kb.begin_kb)
    else:
        await message.answer(texts.use_buttons, reply_markup=kb.send_kb)


