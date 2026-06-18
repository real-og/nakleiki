from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import buttons


# def get_city_recommendation_kb(cities):
#     if cities is None:
#         return None
#     kb = InlineKeyboardMarkup()
#     for city in cities:
#         button = InlineKeyboardButton(text=city, callback_data=city)
#         kb.add(button)
#     return kb

# def get_type_work_recommendation_kb(type_work_variants):
#     if type_work_variants is None:
#         return None
#     kb = InlineKeyboardMarkup()
#     for type_work in type_work_variants:
#         button = InlineKeyboardButton(text=type_work, callback_data=type_work)
#         kb.add(button)
#     return kb

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

# def get_type_transport_recommendation_kb(type_transport_variants):
#     if type_transport_variants is None:
#         return None
#     kb = InlineKeyboardMarkup()
#     for type_transport in type_transport_variants:
#         button = InlineKeyboardButton(text=type_transport, callback_data=type_transport)
#         kb.add(button)
#     return kb

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

send_kb = ReplyKeyboardMarkup([[buttons.send, buttons.reset]],
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

city_kb = InlineKeyboardMarkup()
city_kb.add(InlineKeyboardButton(text=buttons.minsk, callback_data=buttons.minsk))
city_kb.add(InlineKeyboardButton(text=buttons.vitebsk, callback_data=buttons.vitebsk))
city_kb.add(InlineKeyboardButton(text=buttons.brest, callback_data=buttons.brest))
city_kb.add(InlineKeyboardButton(text=buttons.gomel, callback_data=buttons.gomel))
city_kb.add(InlineKeyboardButton(text=buttons.grodno, callback_data=buttons.grodno))
city_kb.add(InlineKeyboardButton(text=buttons.mogilev, callback_data=buttons.mogilev))

type_transport_kb = InlineKeyboardMarkup()
type_transport_kb.add(InlineKeyboardButton(text=buttons.route_taxi, callback_data='route_taxi'))
type_transport_kb.add(InlineKeyboardButton(text=buttons.taxi, callback_data='taxi'))
type_transport_kb.add(InlineKeyboardButton(text=buttons.public_transport, callback_data='public_transport'))
type_transport_kb.add(InlineKeyboardButton(text=buttons.commercial, callback_data='commercial'))
type_transport_kb.add(InlineKeyboardButton(text=buttons.a1, callback_data='a1'))

work_type_kb = InlineKeyboardMarkup()
work_type_kb.add(InlineKeyboardButton(text=buttons.montage, callback_data='montage'))
work_type_kb.add(InlineKeyboardButton(text=buttons.demontage, callback_data='demontage'))
work_type_kb.add(InlineKeyboardButton(text=buttons.repair, callback_data='repair'))

work_type_tracking_kb = InlineKeyboardMarkup()
work_type_tracking_kb.add(InlineKeyboardButton(text=buttons.montage, callback_data='montage'))
work_type_tracking_kb.add(InlineKeyboardButton(text=buttons.demontage, callback_data='demontage'))

taxi_montage_kb = InlineKeyboardMarkup()
taxi_montage_kb.add(InlineKeyboardButton(text=buttons.taxi_montage_1, callback_data='taxi_montage_1'))
taxi_montage_kb.add(InlineKeyboardButton(text=buttons.taxi_montage_2, callback_data='taxi_montage_2'))
taxi_montage_kb.add(InlineKeyboardButton(text=buttons.taxi_montage_3, callback_data='taxi_montage_3'))
taxi_montage_kb.add(InlineKeyboardButton(text=buttons.taxi_montage_4, callback_data='taxi_montage_4'))
taxi_montage_kb.add(InlineKeyboardButton(text=buttons.taxi_montage_5, callback_data='taxi_montage_5'))
taxi_montage_kb.add(InlineKeyboardButton(text=buttons.taxi_montage_6, callback_data='taxi_montage_6'))

taxi_demontage_kb = InlineKeyboardMarkup()
taxi_demontage_kb.add(InlineKeyboardButton(text=buttons.taxi_demontage_1, callback_data='taxi_demontage_1'))
taxi_demontage_kb.add(InlineKeyboardButton(text=buttons.taxi_demontage_2, callback_data='taxi_demontage_2'))
taxi_demontage_kb.add(InlineKeyboardButton(text=buttons.taxi_demontage_3, callback_data='taxi_demontage_3'))
taxi_demontage_kb.add(InlineKeyboardButton(text=buttons.taxi_demontage_4, callback_data='taxi_demontage_4'))

route_montage_kb = InlineKeyboardMarkup()
route_montage_kb.add(InlineKeyboardButton(text=buttons.route_montage_1, callback_data='route_montage_1'))
route_montage_kb.add(InlineKeyboardButton(text=buttons.route_montage_2, callback_data='route_montage_2'))

route_demontage_kb = InlineKeyboardMarkup()
route_demontage_kb.add(InlineKeyboardButton(text=buttons.route_demontage_1, callback_data='route_demontage_1'))
route_demontage_kb.add(InlineKeyboardButton(text=buttons.route_demontage_2, callback_data='route_demontage_2'))
route_demontage_kb.add(InlineKeyboardButton(text=buttons.route_demontage_3, callback_data='route_demontage_3'))

bus_montage_kb = InlineKeyboardMarkup()
bus_montage_kb.add(InlineKeyboardButton(text=buttons.bus_montage_1, callback_data='bus_montage_1'))
bus_montage_kb.add(InlineKeyboardButton(text=buttons.bus_montage_2, callback_data='bus_montage_2'))
bus_montage_kb.add(InlineKeyboardButton(text=buttons.bus_montage_3, callback_data='bus_montage_3'))

bus_demontage_kb = InlineKeyboardMarkup()
bus_demontage_kb.add(InlineKeyboardButton(text=buttons.bus_demontage_1, callback_data='bus_demontage_1'))
bus_demontage_kb.add(InlineKeyboardButton(text=buttons.bus_demontage_2, callback_data='bus_demontage_2'))
bus_demontage_kb.add(InlineKeyboardButton(text=buttons.bus_demontage_3, callback_data='bus_demontage_3'))
bus_demontage_kb.add(InlineKeyboardButton(text=buttons.bus_demontage_4, callback_data='bus_demontage_4'))
bus_demontage_kb.add(InlineKeyboardButton(text=buttons.bus_demontage_5, callback_data='bus_demontage_5'))
bus_demontage_kb.add(InlineKeyboardButton(text=buttons.bus_demontage_6, callback_data='bus_demontage_6'))


def get_active_tasks_kb(active_tasks):
    kb = InlineKeyboardMarkup()
    for task in active_tasks:
        text = task[9] + ' ' + task[5]
        kb.add(InlineKeyboardButton(text=text, callback_data=task[5]))
    return kb

chehly_task_kb = ReplyKeyboardMarkup([[buttons.finish_chehly, buttons.tasks_chehly]],
                                    resize_keyboard=True,
                                    one_time_keyboard=True)


