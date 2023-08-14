LEXICON_COMMANDS = {
    '/start': 'Записаться к мастеру',
    '/help': 'Узнать все доступные вам команды'
}

LEXICON_admin = {
    '/start': 'Здравствуйте! Давайте сделаем вам график работы?\n\nСписок всех команд - /help',
    'no_button_press': 'Жаль!\nЕсли вдруг передумаете - введите команду /start',
    'yes_button_press': 'Отлично!\n\nТеперь укажите год с которого планируете принимать записи!\n\nЭто нужно для того, чтобы правильно сформировать дни и недели в вашем будущем графике работы.',
    'month_button_press': 'Супер!\nДавайте выберем даты, в которые вы планируете работать в этом месяце!',
    'year_wrote': 'Спасибо!\nВведите месяц с которого планируете принимать записи!',
    'bad_month_button_press': 'Пожалуйста, выберите даты в которые вы будете работать',
    'good_month_button_press': 'Отлично!\nТеперь укажите в какое время вы планируете работать в этот день',
    'time_button_press': 'Супер!\nЕсли хотите - выберете еще время, когда планируете принимать клиентов, или нажмите подтвердить',
    'accept_button_press': 'Спасибо!\n\nЕсли желаете посмотреть список всех доступных вам команд - введите команду /help',
    'check_my_working_dates': 'Чтобы отредактировать свой график введите команду /edit_my_working_dates',
    'no_records_in_database': 'Вы ещё не сделали никаких записей!\n\nЧтобы это исправить - введите\n/start или /add_new_working_date',
    'edit_working_date': 'Выберите даты, в которые вы не будете работать'
}

months = {
    1: 'Январь',
    2: 'Февраль',
    3: 'Март',
    4: 'Апрель',
    5: 'Май',
    6: 'Июнь',
    7: 'Июль',
    8: 'Август',
    9: 'Сентябрь',
    10: 'Октябрь',
    11: 'Ноябрь',
    12: 'Декабрь'
}

backward_forward = {
    '<<': 'backward',
    '>>' : 'forward'
}

days_of_the_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

LEXICON_admin_commands = {
    '/start': 'Составить свой график работы',
    '/check_my_working_dates': 'Посмотреть все ваши рабочие дни',
    '/edit_my_working_dates': 'Редактировать ваш график работы.Следует изменять, когда запись или отменена, или клиента обслужили и запись окончена',
    '/add_new_working_date': 'Добавить новый день в ваш график работы',
    '/help': 'Команда показывает список всех команд'
}