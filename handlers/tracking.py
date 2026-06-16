import uuid
import os
import asyncio
from datetime import datetime
from collections import defaultdict

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

import sheets
import texts_tracking
import buttons
import side_logic
import config_io
import keyboards as kb
from states import State
from loader import dp, bot


MIN_AFTER_PHOTOS_TRACKING = 2

USER_PHOTO_LOCKS = defaultdict(asyncio.Lock)


CALLBACK_TEXT_TRACKING = {
    "montage": buttons.montage,
    "demontage": buttons.demontage,
    "repair": buttons.repair,
}


@dp.message_handler(state=State.entering_city_tracking)
async def entering_city_tracking(message: types.Message, state: FSMContext):
    city = message.text

    await state.update_data(city=city)
    await state.update_data(start_date=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    await message.answer(texts_tracking.enter_type_work, reply_markup=kb.work_type_tracking_kb)
    await State.entering_type_work_tracking.set()


@dp.callback_query_handler(state=State.entering_city_tracking)
async def entering_city_tracking_callback(callback: types.CallbackQuery, state: FSMContext):
    city = callback.data

    await state.update_data(city=city)
    await state.update_data(start_date=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    await callback.message.answer(texts_tracking.enter_type_work, reply_markup=kb.work_type_tracking_kb)
    await State.entering_type_work_tracking.set()

    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)


@dp.message_handler(state=State.entering_type_work_tracking)
async def entering_type_work_tracking(message: types.Message, state: FSMContext):
    type_work = message.text

    await state.update_data(type_work=type_work)

    await message.answer(texts_tracking.enter_transport_number, reply_markup=ReplyKeyboardRemove())
    await State.entering_transport_number_tracking.set()


@dp.callback_query_handler(state=State.entering_type_work_tracking)
async def entering_type_work_tracking_callback(callback: types.CallbackQuery, state: FSMContext):
    type_work = CALLBACK_TEXT_TRACKING.get(callback.data, callback.data)

    await state.update_data(type_work=type_work)

    await callback.message.answer(texts_tracking.enter_transport_number, reply_markup=ReplyKeyboardRemove())
    await State.entering_transport_number_tracking.set()

    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)


@dp.message_handler(state=State.entering_transport_number_tracking)
async def entering_transport_number_tracking(message: types.Message, state: FSMContext):
    transport_number = message.text
    transport_number = side_logic.normalize_belarus_plate(transport_number)

    if transport_number is None:
        await message.answer(texts_tracking.bad_plate)
        await message.answer(texts_tracking.enter_transport_number)
        return

    await state.update_data(transport_number=transport_number)

    await message.answer(texts_tracking.enter_tracker_number)
    await State.entering_tracker_number_tracking.set()


@dp.message_handler(state=State.entering_tracker_number_tracking)
async def entering_tracker_number_tracking(message: types.Message, state: FSMContext):
    tracker_number = message.text

    await state.update_data(tracker_number=tracker_number)

    await message.answer(texts_tracking.enter_photos_after)
    await State.entering_photos_after_tracking.set()


@dp.message_handler(content_types=["any"], state=State.entering_photos_after_tracking)
async def entering_photos_after_tracking(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    async with USER_PHOTO_LOCKS[user_id]:
        data = await state.get_data()

        photos_after_tracking = data.get("photos_after_tracking", [])
        photos_after_tracking_pic = data.get("photos_after_tracking_pic", [])
        photos_after_tracking_doc = data.get("photos_after_tracking_doc", [])

        if message.photo or message.document:

            if message.photo:
                photo = message.photo[-1]
                file_id = message.photo[-1].file_id

                photos_after_tracking_pic.append(file_id)

                filename = f"{uuid.uuid4().hex}.jpg"
                path = "photos/" + filename

                await photo.download(destination_file=str(path))

            elif message.document:
                doc = message.document

                if not doc.mime_type or not doc.mime_type.startswith("image/"):
                    await message.answer(texts_tracking.error_photo)
                    return

                file_id = message.document.file_id

                photos_after_tracking_doc.append(file_id)

                ext = os.path.splitext(doc.file_name or "")[1] or ".jpg"
                filename = f"{uuid.uuid4().hex}{ext}"
                path = "photos/" + filename

                await doc.download(destination_file=str(path))

            photos_after_tracking.append(filename)

            photos_count = len(photos_after_tracking)

            await state.update_data(photos_after_tracking=photos_after_tracking)
            await state.update_data(photos_after_tracking_pic=photos_after_tracking_pic)
            await state.update_data(photos_after_tracking_doc=photos_after_tracking_doc)

            if photos_count <= MIN_AFTER_PHOTOS_TRACKING:
                await message.answer(f"Принято {photos_count}/{MIN_AFTER_PHOTOS_TRACKING} фото.")

            if photos_count == MIN_AFTER_PHOTOS_TRACKING:
                await message.answer(texts_tracking.enter_comment, reply_markup=kb.skip_comment_kb)
                await State.entering_comment_tracking.set()
                await state.update_data(end_date=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

            if photos_count > MIN_AFTER_PHOTOS_TRACKING:
                await message.answer(f"Принято дополнительное {photos_count}/{MIN_AFTER_PHOTOS_TRACKING} фото.")

        else:
            await message.answer(texts_tracking.error_photo)


@dp.message_handler(state=State.entering_comment_tracking)
async def entering_comment_tracking(message: types.Message, state: FSMContext):
    comment = message.text

    skip_comment = getattr(buttons, "skip_comment", None)
    if skip_comment and comment == skip_comment:
        comment = ""

    await state.update_data(comment=comment)

    data = await state.get_data()

    report = texts_tracking.generate_report(data)

    await message.answer(report)

    await side_logic.send_files_by_ids_album(
        message,
        data.get("photos_after_tracking_pic"),
        data.get("photos_after_tracking_doc"),
        texts_tracking.photos_after
    )

    await message.answer(texts_tracking.enter_finish, reply_markup=kb.send_kb)

    await State.last_check_tracking.set()


@dp.message_handler(state=State.last_check_tracking)
async def last_check_tracking(message: types.Message, state: FSMContext):
    if message.text == buttons.send:
        data = await state.get_data()

        await message.answer("Отправляем, немного подождите")

        report = texts_tracking.generate_report(data)

        await bot.send_message(config_io.get_value("CHAT_ID_TRACKING"), report)

        await side_logic.send_files_by_ids_album(
            message,
            data.get("photos_after_tracking_pic"),
            data.get("photos_after_tracking_doc"),
            texts_tracking.photos_after,
            bot,
            config_io.get_value("CHAT_ID_TRACKING")
        )

        row_data = side_logic.form_list_to_append_tracking(message.from_user.id, data)
        await sheets.append_row_to_trackers_notes(row_data)

        await state.finish()

        await message.answer(texts_tracking.result_saved)
        await message.answer(texts_tracking.enter_city, reply_markup=kb.city_kb)
        await State.entering_city_tracking.set()

        user = await sheets.get_user(message.from_user.id)
        await state.update_data(worker_number=user[2])
        await state.update_data(worker_name=user[3])
        

    elif message.text == buttons.reset:
        await message.answer("Данные по этому трекеру сброшены")

        await state.finish()

        await message.answer(texts_tracking.enter_city, reply_markup=kb.city_kb)
        await State.entering_city_tracking.set()

        user = await sheets.get_user(message.from_user.id)
        await state.update_data(worker_number=user[2])
        await state.update_data(worker_name=user[3])

    else:
        await message.answer(texts_tracking.use_buttons, reply_markup=kb.send_kb)