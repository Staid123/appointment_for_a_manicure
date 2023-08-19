import calendar


def check_phone_number(phone_number) -> bool:
    if phone_number.isdigit() and len(phone_number) == 10 and str(phone_number)[0] == '0':
        return True
    return False



def day_in_months(year: str, month: int) -> list:
    result = []
    zero_days_calendar = calendar.Calendar().itermonthdays(int(year), int(month))
    for i in zero_days_calendar:
        if i == 0:
            result += ['-']
        else:
            result += [i]
    return result


def working_time_in_day() -> list:
    time = '8:00'
    lst: list = [time]
    while time != '18:00':
        if str(int(time[-2:]) + 15) != '60':
            hour = time.split(':')[0]
            minutes = str(int(time[-2:]) + 15)
        else:
            hour = str(int(time.split(':')[0]) + 1)
            minutes = '00'
        time = hour + ':' + minutes
        lst.append(time)
    return lst



def format_func1(dct: dict) -> str:
    res: str = str()
    for command, text in dct.items():
        res += (f'{command}\n{text}\n\n')
    return res


def format_func2(lst: list, months: dict) -> str:
    res = 'К вам записаны:\n\n\n'
    for tupl in lst:
        month = months[tupl[3]].lower()
        if month[-1] in ['ь', 'й']:
            month = month.replace(month[-1], 'я')
        else:
            month += 'а'
        res += f'{tupl[0]} на {tupl[-1]} {tupl[4]} {month} {tupl[2]} года.\nНомер телефона клиента: {tupl[1]}\n\n'
    return res