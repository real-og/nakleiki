from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import buttons


def get_number_recommendation_kb(phone_number):
    if phone_number:
        return ReplyKeyboardMarkup([[str(phone_number)]],
                                    resize_keyboard=True,
                                    one_time_keyboard=True)
    return None

def get_city_recommendation_kb(cities):
    if cities is None:
        return None
    kb = InlineKeyboardMarkup()
    for city in cities:
        button = InlineKeyboardButton(text=city, callback_data=city)
        kb.add(button)
    return kb

def get_type_work_recommendation_kb(type_work_variants):
    if type_work_variants is None:
        return None
    kb = InlineKeyboardMarkup()
    for type_work in type_work_variants:
        button = InlineKeyboardButton(text=type_work, callback_data=type_work)
        kb.add(button)
    return kb

def get_narrative_recommendation_kb(narrative_variants):
    if narrative_variants is None:
        return None
    kb = InlineKeyboardMarkup()
    for narrative in narrative_variants:
        button = InlineKeyboardButton(text=narrative, callback_data=narrative)
        kb.add(button)
    return kb

def get_type_transport_recommendation_kb(type_transport_variants):
    if type_transport_variants is None:
        return None
    kb = InlineKeyboardMarkup()
    for type_transport in type_transport_variants:
        button = InlineKeyboardButton(text=type_transport, callback_data=type_transport)
        kb.add(button)
    return kb


completed_work_kb = ReplyKeyboardMarkup([['Выполнено', 'Не выполнено']],
                                    resize_keyboard=True,
                                    one_time_keyboard=True)


