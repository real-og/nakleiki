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
import texts_chehly
import config_io
import keyboards as kb
from states import State
from loader import dp, bot


MIN_AFTER_PHOTOS_CHEHLY = 3

USER_PHOTO_LOCKS = defaultdict(asyncio.Lock)



@dp.callback_query_handler(state=State.entering_active_task)
async def entering_city_tracking_callback(callback: types.CallbackQuery, state: FSMContext):
    task_auto_number = callback.data
    await state.update_data(task_now=task_auto_number)

    data = await state.get_data()
    selected_task = None
    active_tasks = data.get('active_tasks', [])
    for task in active_tasks:
        if task[5] == task_auto_number:
            selected_task = task
            break

    text = texts_chehly.generate_task_text(selected_task)
    await callback.message.answer(text, reply_markup=kb.chehly_task_kb)
    await callback.message.edit_reply_markup(reply_markup=None)

    await State.opened_task.set()


@dp.message_handler(state=State.opened_task)
async def send_welcome(message: types.Message, state: FSMContext):
    user_input = message.text

    data = await state.get_data()

    task_auto_number = data.get('task_now')
    selected_task = None
    active_tasks = data.get('active_tasks', [])

    for task in active_tasks:
        if task[5] == task_auto_number:
            selected_task = task
            break

    if user_input == buttons.finish_chehly:
        photos_count = len(selected_task[21])
        if photos_count >= MIN_AFTER_PHOTOS_CHEHLY:
            await message.answer(texts_chehly.task_completed)

            tasks = data.get('active_tasks')
            await state.update_data(active_tasks=active_tasks)
            active_tasks = []
            selected_task[20] = 'completed'
            for task in tasks:
                if task[20] != 'completed':
                    active_tasks.append(task)
            await message.answer(texts_chehly.active_tasks, reply_markup=kb.get_active_tasks_kb(active_tasks))
            await State.entering_active_task.set()

            
            report = texts_chehly.generate_task_text(selected_task)
            await bot.send_message(config_io.get_value('CHAT_ID_CHEHLY'), report)
            photos_ids = selected_task[21]
            await side_logic.send_files_by_ids_album(message, photos_ids, [], texts_chehly.photos_pinned, bot, config_io.get_value('CHAT_ID_CHEHLY'))

            await sheets.replace_task_row_by_key(selected_task)


        else:
            await message.answer(texts_chehly.not_enough_photos, reply_markup=kb.chehly_task_kb)


    elif user_input == buttons.tasks_chehly:
        tasks = data.get('active_tasks')
        active_tasks = []
        for task in tasks:
            if task[20] != 'completed':
                active_tasks.append(task)
        await message.answer(texts_chehly.active_tasks, reply_markup=kb.get_active_tasks_kb(active_tasks))
        await State.entering_active_task.set()
    else:
        comment = user_input
        for task in active_tasks:
            if task[5] == task_auto_number:
                task[18] = comment
                break
        selected_task[18] = comment
        await state.update_data(active_tasks=active_tasks)
        await message.answer(texts_chehly.comment_added)
        text = texts_chehly.generate_task_text(selected_task)

        await message.answer(text, reply_markup=kb.chehly_task_kb)



@dp.message_handler(content_types=['any'], state=State.opened_task)
async def handle_photo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    async with USER_PHOTO_LOCKS[user_id]:
        data = await state.get_data()
        task_auto_number = data.get('task_now')
        selected_task = None
        active_tasks = data.get('active_tasks', [])
        for task in active_tasks:
            if task[5] == task_auto_number:
                selected_task = task
                break

        photos_after_pic = selected_task[21]

        if message.photo:
            photo = message.photo[-1]
            file_id = message.photo[-1].file_id
            photos_after_pic.append(file_id)
            filename = f"{uuid.uuid4().hex}.jpg"
            path = 'photos_chehly/' + filename
            await photo.download(destination_file=str(path))
            selected_task[19] = len(selected_task[21])
            await state.update_data(active_tasks=active_tasks)

            photos_count = len(selected_task[21])
            if photos_count <= MIN_AFTER_PHOTOS_CHEHLY:
                await message.answer(f"Принято {photos_count}/{MIN_AFTER_PHOTOS_CHEHLY} фото.")
            if photos_count == MIN_AFTER_PHOTOS_CHEHLY:
                await message.answer(f"Нужное количество фото достигнуто, можно завершать задание")
            if photos_count > MIN_AFTER_PHOTOS_CHEHLY:
                await message.answer(f"Принято дополнительное {photos_count}/{MIN_AFTER_PHOTOS_CHEHLY} фото.")
        else:
            await message.answer(texts_chehly.error_photo)
        



