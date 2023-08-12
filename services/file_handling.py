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
