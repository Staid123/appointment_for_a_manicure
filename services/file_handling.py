import calendar

def day_in_months(year, month):
    result = []
    zero_days_calendar = calendar.Calendar()
    for i in zero_days_calendar:
        if i == 0:
            result += ['-']
        else:
            result += [i]
    return result


