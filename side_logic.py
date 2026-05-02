import re
import os
from datetime import datetime

from aiogram import types
from pathlib import Path
import buttons
import config_io

PHOTO_DIR = Path("photos")


async def send_photos_album(
    message: types.Message,
    photo_names: list[str],
    caption: str = "",
    bot = None

):
    media = []

    for i, name in enumerate(photo_names[:10]):
        path = PHOTO_DIR / name

        media.append(
            types.InputMediaPhoto(
                media=types.InputFile(str(path)),
                caption=caption if i == 0 else None
            )
        )
    if bot:
        await bot.send_media_group(config_io.get_value('CHAT_ID'), media)
    else:
        await message.answer_media_group(media)

def form_list_to_append(id_tg, data):
    result = []
    result.append(data.get('start_date'))
    result.append(data.get('end_date'))
    result.append(id_tg)
    result.append(data.get('worker_number'))
    result.append(data.get('worker_name'))
    result.append(data.get('city'))
    if data.get('type_work') == 'Демонтаж-Монтаж':
        result.append('Демонтаж')
    else:
        result.append(data.get('type_work'))
    result.append(data.get('narrative'))
    result.append(data.get('type_transport'))
    result.append(data.get('transport_number'))
    result.append(data.get('representative'))
    result.append(data.get('route_number'))
    result.append(data.get('is_completed'))
    result.append(len(data.get('photos_passport', [])))
    result.append(len(data.get('photos_before')))
    result.append(len(data.get('photos_after')))
    result.append(data.get('comment'))
    result.append(data.get('working_solo'))
    if data.get('working_solo') == buttons.no:
        result.append(data.get('solo_percent'))
        for i in range(len(data.get('teammates'))):
            result.append(data.get('teammates')[i])
            result.append(data.get('teammates_percent')[i])
    return result


def normalize_phone(phone: str) -> str | None:
    if not isinstance(phone, str):
        return None
    phone = phone.strip()
    if re.fullmatch(r"\+?375\d{9}", phone):
        return phone.lstrip("+")
    return None


def is_int_0_100(value: str) -> bool:
    if not isinstance(value, str):
        return False
    value = value.strip()
    if not value.isdecimal():
        return False
    number = int(value)
    return 0 <= number <= 100

def delete_files_from_folder(filenames: list[str], folder: str) -> None:
    for filename in filenames:
        path = os.path.join(folder, filename)

        if os.path.isfile(path):
            os.remove(path)

async def remake_data_after_demontage(state):
    data = await state.get_data()
    await state.update_data(is_combo=1)
    await state.update_data(type_work='Монтаж')
    await state.update_data(is_completed=-1)
    await state.update_data(photos_before=data.get('photos_after'))
    await state.update_data(photos_after=[])
    await state.update_data(comment=None)
    await state.update_data(working_solo=None)
    await state.update_data(solo_percent=None)
    await state.update_data(teammates=[])
    await state.update_data(teammates_percent=[])



def normalize_belarus_plate(value: str):
    if not isinstance(value, str):
        return None

    ru_to_en = str.maketrans({
        "А": "A",
        "В": "B",
        "Е": "E",
        "К": "K",
        "М": "M",
        "Н": "H",
        "О": "O",
        "Р": "P",
        "С": "C",
        "Т": "T",
        "У": "Y",
        "Х": "X",
    })

    plate = value.strip().upper().replace(" ", "").translate(ru_to_en)

    letters = "ABEKMHOPCTYXI"

    patterns = [
        rf"^[{letters}]{{2}}\d{{4}}-[1-8]$",   # AB9704-7
        rf"^\d{{4}}[{letters}]{{2}}-[1-8]$",   # 9889BA-1
        rf"^E\d{{3}}[{letters}]{{2}}-[1-8]$",  # E001AA-7
        rf"^[{letters}]{{2}}-\d{{5}}$",        # AO-78912
        rf"^\d[{letters}]{{3}}\d{{4}}$",       # 2EHT3624
    ]

    if any(re.fullmatch(pattern, plate) for pattern in patterns):
        return plate

    return None
    
    

