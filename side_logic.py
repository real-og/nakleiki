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
    result = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id_tg]
    result.append(data.get('worker_number'))
    result.append(data.get('worker_name'))
    result.append(data.get('city'))
    result.append(data.get('type_work'))
    result.append(data.get('narrative'))
    result.append(data.get('type_transport'))
    result.append(data.get('representative'))
    result.append(data.get('transport_number'))
    result.append(data.get('route_number'))
    result.append(data.get('is_completed'))
    result.append(len(data.get('photos_passport')))
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