import buttons

start_message = """Бот создан для автоматического трекинга работ по оклейке/ремонту/демонтажу автотранспорта.
Следуйте инструкциям ниже, чтобы отметить свою работу.

/help - для помощи;
/start - начать заново."""

help_message = """Здесь могут быть подсказки"""

enter_your_phone = 'Введите свой номер телефона в формате 375292222222 или выберите из списка ниже, если уже вводили номер ранее.'

enter_your_city = """Выберите город или введите текстом, если Ваш город отсутствует"""
enter_type_work = """Выберите тип работ"""
enter_narrative = """Напишите сюжет"""
enter_type_transport = """Выберите вид транспорта"""
enter_transport_number = """Введите номер машины"""
enter_route_number = """Введите номер маршрута"""
enter_photos_before = """Пришлите фото <b>до работы</b>"""
error_photo = 'Это не похоже на фото'
go_to_work = 'Фото принято, приступайте к работе.'


use_buttons = 'Используйте кнопки ниже'
enter_photos_after = """Пришлите фото <b>после работы</b>"""
enter_comment = """Оставьте комментарий по работе"""
enter_was_solo = """Работу записываем только на Вас?"""
photos_before = 'Фото до работы'
photos_after = 'Фото после работы'
enter_your_percent = "Сколько процентов работы сделали <b>Вы</b>?"
enter_coworker = "Добавьте номер телефона того, кто с Вами работал"
enter_coworker_or_exit = "Добавьте номер телефона того, кто с Вами работал или выберите <b>Закончить</b> добавление"
enter_coworker_percent = "Сколько процентов работы выполнил данный работник?"
enter_finish = """Сверьте результат и нажмите <b>Отправить</b> для завершения заказа"""
result_saved = """Результат сохранен
/start для следующей работы"""

def generate_report(data):

    result = f"""Исполнитель: <b>{data.get('worker')}</b>
Город: <b>{data.get('city')}</b>
Вид работ: <b>{data.get('type_work')}</b>
Сюжет: <b>{data.get('narrative')}</b>
Вид транспорта: <b>{data.get('type_transport')}</b>
Номер машины: <b>{data.get('transport_number')}</b>
Номер маршрута: <b>{data.get('route_number')}</b>
Выполнено: <b>{data.get('is_completed')}</b>
Фотографий до: <b>{len(data.get('photos_before'))}</b>
Фотографий после: <b>{len(data.get('photos_after'))}</b>
Комментарий: <b>{data.get('comment')}</b>
"""
    if data.get('working_solo') == buttons.no:
        result += f"""\nСделал сам <b>{data.get('solo_percent')}</b> процентов\n"""
        for i in range(len(data.get('teammates'))):
            result += f"""Помощник <b>{data.get('teammates')[i]}</b>
Выполнил <b>{data.get('teammates_percent')[i]}</b> процентов\n"""
            
    return result