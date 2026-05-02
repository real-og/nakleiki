from aiogram.dispatcher.filters.state import StatesGroup, State


class State(StatesGroup):
    reg_number = State()
    reg_name = State()
    entering_begin = State()

    entering_your_city = State()
    entering_type_work = State()
    entering_narrative = State()
    entering_type_transport = State()
    entering_representative = State()
    entering_transport_number = State()
    entering_route_number = State()
    entering_photos_passport = State()
    entering_photos_before = State()
    working_on = State()

    entering_photos_after = State()
    entering_comment = State()
    entering_was_working_solo = State()
    entering_my_percent = State()
    adding_coworker = State()
    entering_percent_coworker = State()
    last_check = State()

