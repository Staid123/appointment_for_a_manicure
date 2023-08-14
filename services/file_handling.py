import calendar


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
    lst = ['8:00', '10:00', '12:00', '14:00', '16:00', '18:00']
    return lst


def format_func1(dct: dict) -> str:
    res: str = str()
    for command, text in dct.items():
        res += (f'{command}\n{text}\n\n')
    return res



def format_func2(lst: list, months: dict) -> str:
    res = 'Вы работаете:\n\n'
    for tupl in lst:
        month = months[tupl[1]].lower()
        if month[-1] in ['ь', 'й']:
            month = month.replace(month[-1], 'я')
        else:
            month += 'а'
        res += f'{str(tupl[2])} {month} {str(tupl[0])} в {tupl[-1]}\n'
    return res