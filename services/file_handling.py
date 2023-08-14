import calendar


def day_in_months(year: str, month: int):
    result = []
    zero_days_calendar = calendar.Calendar().itermonthdays(int(year), int(month))
    for i in zero_days_calendar:
        if i == 0:
            result += ['-']
        else:
            result += [i]
    return result


def working_time_in_day():
    lst = ['8:00', '10:00', '12:00', '14:00', '16:00', '18:00']
    return lst

