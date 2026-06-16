import os
import uuid

from aiogram import types
from aiogram.dispatcher import FSMContext

import sheets
import side_logic
from loader import dp
import tracker_complition


EXCEL_DIR = "excel_files"

def is_excel_file(message: types.Message):
    if not message.document:
        return False

    file_name = message.document.file_name or ""
    file_name = file_name.lower()

    return file_name.endswith((".xlsx", ".xlsm"))


@dp.message_handler(is_excel_file, content_types=["document"], state="*")
async def handle_excel_file_from_any_state(message: types.Message, state: FSMContext):
    document = message.document

    os.makedirs(EXCEL_DIR, exist_ok=True)

    original_file_name = document.file_name or "file.xlsx"
    ext = os.path.splitext(original_file_name)[1]

    saved_file_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(EXCEL_DIR, saved_file_name)

    await message.answer("Excel-файл принят. Проверяю номера...")

    try:
        await document.download(destination_file=file_path)

        numbers_by_rows = tracker_complition.get_transport_numbers_from_excel(file_path)

        tracking_rows = await sheets.get_all_values(3)
        tracking_rows = tracking_rows[1:]

        result_text = tracker_complition.generate_excel_tracking_compare_text(
            numbers_by_rows,
            tracking_rows
        )

        await message.answer(result_text)

        if not result_text:
            await message.answer("Не удалось сформировать результат.")
            return

    except Exception as e:
        await message.answer(f"Ошибка при обработке Excel-файла: {e}")

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)