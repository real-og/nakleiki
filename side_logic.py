from aiogram import types
from pathlib import Path

PHOTO_DIR = Path("photos")


async def send_photos_album(
    message: types.Message,
    photo_names: list[str],
    caption: str = ""
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

    await message.answer_media_group(media)