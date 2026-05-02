from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import buttons


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
    if len(narrative_variants) >= 10:
        kb = InlineKeyboardMarkup(row_width=2)
        buttons = [
            InlineKeyboardButton(text=narrative, callback_data=narrative)
            for narrative in narrative_variants
        ]
        kb.add(*buttons)
    else:
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

def get_users_to_select(users):
    if users is None:
        return None
    kb = InlineKeyboardMarkup()
    for user in users:
        number = user[2]
        name = user[3]
        user_compiled = name + ' ' + str(number)
        button = InlineKeyboardButton(text=user_compiled, callback_data=user_compiled)
        kb.add(button)
    return kb


begin_kb = ReplyKeyboardMarkup([[buttons.begin]],
                                    resize_keyboard=True,
                                    one_time_keyboard=True)


completed_work_kb = ReplyKeyboardMarkup([[buttons.completed, buttons.uncompleted]],
                                    resize_keyboard=True,
                                    one_time_keyboard=True)

skip_comment_kb = ReplyKeyboardMarkup([[buttons.skip_comment]],
                                    resize_keyboard=True,
                                    one_time_keyboard=True)

yes_no_kb = ReplyKeyboardMarkup([[buttons.yes, buttons.no]],
                                    resize_keyboard=True,
                                    one_time_keyboard=True)

finish_kb = ReplyKeyboardMarkup([[buttons.finish]],
                                    resize_keyboard=True,
                                    one_time_keyboard=True)

send_kb = ReplyKeyboardMarkup([[buttons.send]],
                                    resize_keyboard=True,
                                    one_time_keyboard=True)

no_info_kb = ReplyKeyboardMarkup([[buttons.no_info]],
                                    resize_keyboard=True,
                                    one_time_keyboard=True)

def get_percent_kb():
    kb = InlineKeyboardMarkup(row_width=3)
    kb.add(
        InlineKeyboardButton(text="10", callback_data="10"),
        InlineKeyboardButton(text="20", callback_data="20"),
        InlineKeyboardButton(text="30", callback_data="30"),
        InlineKeyboardButton(text="40", callback_data="40"),
        InlineKeyboardButton(text="50", callback_data="50"),
        InlineKeyboardButton(text="60", callback_data="60"),
        InlineKeyboardButton(text="70", callback_data="70"),
        InlineKeyboardButton(text="80", callback_data="80"),
        InlineKeyboardButton(text="90", callback_data="90"),
    )
    return kb
