import buttons

start_message = """Бот создан для автоматического трекинга работ по оклейке/ремонту/демонтажу автотранспорта.
Следуйте инструкциям ниже, чтобы отметить свою работу.

/help - для помощи;
/start - начать заново."""

enter_begin = "Можете приступать к работе. Чтобы начать используйте кнопку ниже или вводите <b>Приступить</b>"
begin_tapped = 'Приступаем'
reg_number = """<b>Регистрация</b>

Для начала введите свой номер телефона в формате 375292222222.
Вам нужно сделать это только один раз"""

bad_number = 'Что-то не так. Введите в формате двеннадцати цифр, например 375292222222.'

reg_name = """Введите свое имя."""

reg_ended = """Регистрация завершена. Можете приступать к работе. Чтобы начать используйте кнопку ниже или вводите <b>Приступить</b>"""

help_message = """Если что-то пошло не так или хотите изменить свой номер/имя, пишите @nik_name3333
/start - чтобы начать заполнение заново."""

enter_your_city = """Выберите город или введите текстом, если Ваш город отсутствует"""
enter_type_work = """Выберите тип работ"""
enter_narrative = """Выберите сюжет"""
enter_type_transport = """Выберите вид транспорта"""
enter_transport_number = """Введите автомобильный номер.
Формат должен соответствовать чему-то из:

<b>AB9704-7</b>
<b>9889BA-1</b>
<b>E001AA-7</b>
<b>AO-78912</b>
<b>2EHT3624</b>"""
enter_route_number = """Введите номер маршрута"""
enter_photos_passport = """Пришлите фото <b>техпаспорта</b>
Требуется 2 фото"""
enter_photos_before = """Пришлите фото <b>до работы</b>
Требуется 4 фото"""
error_photo = 'Это не похоже на фото'
go_to_work = 'Фото принято, приступайте к работе.'
narrative_accepted_go_to_montage = 'Сюжет монтажа сохранен, приступайте к работе'


use_buttons = 'Используйте кнопки ниже'
enter_photos_after = """Пришлите фото <b>после работы</b>
Требуется 4 фото"""
enter_comment = """Оставьте комментарий по работе"""
enter_was_solo = """Работу записываем <b>только на Вас?</b> 
Далее можно будет добавить одного коллегу."""
photos_passport = 'Фото техпаспорта'
photos_before = 'Фото до'
photos_after = 'Фото после'
enter_your_percent = "Сколько процентов работы сделали <b>Вы</b>?"
bad_percent = "Введите целое число от 0 до 100 - сколько процентов работы выполнили <b>Вы</b>."
enter_coworker = "Выберите из списка работника, с которым работали. Он должен быть зарегистрирован"
coworker_percent = "Этот работник выполнил в процентах: "
enter_finish = """Сверьте результат и нажмите <b>Отправить</b> для завершения заказа"""
result_saved = """Результат сохранен. Можете приступать к следующей работе. Нажимайте или вводите <b>Приступить</b>"""
result_saved_demontage = "Результат демонтажа сохранен, выбирайте сюжет монтажа"
def generate_report(data):
    if data.get('representative'):
        representative_row = f"\nЮр.лицо: <b>{data.get('representativer')}</b>"
    else:
        representative_row = ''
    
    if data.get('type_work') == 'Демонтаж-Монтаж':
        type_work = 'часть Демонтаж из Демонтаж-Монтаж'
    else:
        type_work = data.get('type_work')


        
    result = f"""Исполнитель: <b>{data.get('worker_name')}</b>
Номер исполнителя: <b>{data.get('worker_number')}</b>
Город: <b>{data.get('city')}</b>
Вид работ: <b>{type_work}</b>
Сюжет: <b>{data.get('narrative')}</b>
Вид транспорта: <b>{data.get('type_transport')}</b>
Номер машины: <b>{data.get('transport_number')}</b>{representative_row}
Номер маршрута: <b>{data.get('route_number')}</b>
Выполнено: <b>{data.get('is_completed')}</b>
Фотографий техпаспорта: <b>{len(data.get('photos_passport', []))}</b>
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



photo_need_reached = 'Нужное количество фото достигнуто'

enter_representative = "Напишите юр.лицо перевозчика"

go_to_demontage = 'Фото принято, приступайте к <b>демонтажу</b>'
enter_photos_before_demontage = """Пришлите фото до <b>демонтажа</b>
Требуется 4 фото"""
enter_photos_after_demontage = """Пришлите фото после <b>демонтажа</b>
Требуется 4 фото
"""
enter_comment_demontage = "Напишите комментарий по <b>демонтажу</b>"
enter_was_solo_demontage = """Демонтаж записываем <b>только на Вас?</b> 
Далее можно будет добавить одного коллегу."""


enter_coworker_demontage = "Выберите из списка работника, с которым выполняли демонтаж. Он должен быть зарегистрирован"

enter_finish_demontage = 'Сверьте результат, отправьте информацию по <b>демонтажу</b> и приступайте к монтажу.'
bad_plate = 'Неверный формат'