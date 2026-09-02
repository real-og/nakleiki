from aiogram import types
from aiogram.dispatcher import FSMContext

import buttons
import constants
import keyboards as kb
import navigation
import sheets
import texts

from loader import dp
from states import State

from telegram_safe import (
    safe_answer,
    safe_callback_answer,
    safe_edit_reply_markup,
)


async def return_to_previous_state(
    message: types.Message,
    state: FSMContext,
):
    previous_state = await navigation.pop_state(state)

    if previous_state is None:
        await safe_answer(message, "Назад вернуться нельзя.")
        return

    data = await state.get_data()

    # =========================
    # ГОРОД
    # =========================

    if previous_state == State.entering_your_city.state:
        await state.update_data(city=None)

        await state.set_state(
            State.entering_your_city.state
        )

        await safe_answer(
            message,
            texts.enter_your_city,
            reply_markup=kb.get_city_recommendation_kb(
                constants.cities
            )
        )

        return

    # =========================
    # ТИП РАБОТЫ
    # =========================

    if previous_state == State.entering_type_work.state:
        await state.update_data(type_work=None)

        await state.set_state(
            State.entering_type_work.state
        )

        await safe_answer(
            message,
            texts.enter_type_work,
            reply_markup=kb.get_type_work_recommendation_kb(
                constants.type_work
            )
        )

        return

    # =========================
    # НАРРАТИВ
    # =========================

    if previous_state == State.entering_narrative.state:
        await state.update_data(narrative=None)

        await state.set_state(
            State.entering_narrative.state
        )

        text_to_answer = texts.enter_narrative

        if data.get("type_work") == "Демонтаж-Монтаж":
            text_to_answer += "<b> демонтажа</b>"

        await safe_answer(
            message,
            text_to_answer,
            reply_markup=kb.get_narrative_recommendation_kb(
                constants.narrative
            )
        )

        return

    # =========================
    # ТИП ТРАНСПОРТА
    # =========================

    if previous_state == State.entering_type_transport.state:
        await state.update_data(type_transport=None)

        await state.set_state(
            State.entering_type_transport.state
        )

        await safe_answer(
            message,
            texts.enter_type_transport,
            reply_markup=kb.get_type_transport_recommendation_kb(
                constants.type_transport
            )
        )

        return

    # =========================
    # НОМЕР ТРАНСПОРТА
    # =========================

    if previous_state == State.entering_transport_number.state:
        await state.update_data(transport_number=None)

        await state.set_state(
            State.entering_transport_number.state
        )

        await safe_answer(
            message,
            texts.enter_transport_number,
            reply_markup=kb.back_kb
        )

        return

    # =========================
    # ПРЕДСТАВИТЕЛЬ
    # =========================

    if previous_state == State.entering_representative.state:
        await state.update_data(representative=None)

        await state.set_state(
            State.entering_representative.state
        )

        await safe_answer(
            message,
            texts.enter_representative,
            reply_markup=kb.no_info_kb
        )

        return

    # =========================
    # НОМЕР МАРШРУТА
    # =========================

    if previous_state == State.entering_route_number.state:
        await state.update_data(route_number=None)

        await state.set_state(
            State.entering_route_number.state
        )

        await safe_answer(
            message,
            texts.enter_route_number,
            reply_markup=kb.back_kb
        )

        return

    # =========================
    # ФОТО ПАСПОРТА
    # =========================

    if previous_state == State.entering_photos_passport.state:
        await state.update_data(
            photos_passport=[],
            photos_passport_pic=[],
            photos_passport_doc=[],
        )

        await state.set_state(
            State.entering_photos_passport.state
        )

        await safe_answer(
            message,
            texts.enter_photos_passport,
            reply_markup=kb.no_info_kb
        )

        return

    # =========================
    # ФОТО ДО
    # =========================

    if previous_state == State.entering_photos_before.state:
        await state.update_data(
            photos_before=[],
            photos_before_pic=[],
            photos_before_doc=[],
        )

        await state.set_state(
            State.entering_photos_before.state
        )

        if data.get("type_work") == "Демонтаж-Монтаж":
            await safe_answer(
                message,
                texts.enter_photos_before_demontage,
                reply_markup=kb.back_kb
            )

        else:
            text = (
                f"<i>{data.get('type_work')}\n\n</i>"
                + texts.enter_photos_before
            )

            await safe_answer(
                message,
                text,
                reply_markup=kb.back_kb
            )

        return

    # =========================
    # РАБОТА
    # =========================

    if previous_state == State.working_on.state:
        await state.update_data(is_completed=None)

        await state.set_state(
            State.working_on.state
        )

        if data.get("is_combo"):
            text = texts.narrative_accepted_go_to_montage

        elif data.get("type_work") == "Демонтаж-Монтаж":
            text = texts.go_to_demontage

        else:
            text = texts.go_to_work

        await safe_answer(
            message,
            text,
            reply_markup=kb.completed_work_kb
        )

        return

    # =========================
    # ФОТО ПОСЛЕ
    # =========================

    if previous_state == State.entering_photos_after.state:
        await state.update_data(
            photos_after=[],
            photos_after_pic=[],
            photos_after_doc=[],
            end_date=None,
        )

        await state.set_state(
            State.entering_photos_after.state
        )

        if data.get("type_work") == "Демонтаж-Монтаж":
            await safe_answer(
                message,
                texts.enter_photos_after_demontage,
                reply_markup=kb.back_kb
            )

        else:
            text = (
                f"<i>{data.get('type_work')}\n\n</i>"
                + texts.enter_photos_after
            )

            await safe_answer(
                message,
                text,
                reply_markup=kb.back_kb
            )

        return

    # =========================
    # КОММЕНТАРИЙ
    # =========================

    if previous_state == State.entering_comment.state:
        await state.update_data(comment=None)

        await state.set_state(
            State.entering_comment.state
        )

        if data.get("type_work") == "Демонтаж-Монтаж":
            text = texts.enter_comment_demontage
        else:
            text = texts.enter_comment

        await safe_answer(
            message,
            text,
            reply_markup=kb.skip_comment_kb
        )

        return

    # =========================
    # РАБОТАЛ ОДИН?
    # =========================

    if previous_state == State.entering_was_working_solo.state:
        await state.update_data(working_solo=None)

        await state.set_state(
            State.entering_was_working_solo.state
        )

        if data.get("type_work") == "Демонтаж-Монтаж":
            text = texts.enter_was_solo_demontage
        else:
            text = texts.enter_was_solo

        await safe_answer(
            message,
            text,
            reply_markup=kb.yes_no_kb
        )

        return

    # =========================
    # МОЙ ПРОЦЕНТ
    # =========================

    if previous_state == State.entering_my_percent.state:
        await state.update_data(solo_percent=None)

        await state.set_state(
            State.entering_my_percent.state
        )

        await safe_answer(
            message,
            texts.enter_your_percent,
            reply_markup=kb.get_percent_kb()
        )

        return

    # =========================
    # ВЫБОР КОЛЛЕГИ
    # =========================

    if previous_state == State.adding_coworker.state:
        await state.update_data(
            teammates=[],
            teammates_percent=[],
        )

        await state.set_state(
            State.adding_coworker.state
        )

        users = await sheets.get_users()

        if data.get("type_work") == "Демонтаж-Монтаж":
            text = texts.enter_coworker_demontage
        else:
            text = texts.enter_coworker

        await safe_answer(
            message,
            text,
            reply_markup=kb.get_users_to_select(users)
        )

        return
    






@dp.message_handler(lambda message: message.text == buttons.back, state="*")
async def go_back_message(message: types.Message, state: FSMContext):
    await return_to_previous_state(
        message,
        state
    )


@dp.callback_query_handler(lambda callback: callback.data == 'back', state="*")
async def go_back_callback(callback: types.CallbackQuery, state: FSMContext,):
    await safe_callback_answer(callback)
    try:
        await safe_edit_reply_markup(
            callback.message,
            reply_markup=None
        )
    except Exception:
        pass
    await return_to_previous_state(
        callback.message,
        state
    )