"""
the module contains a function for generating search dates
:function:
get_date - forms the start and end date of the search
"""
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar


def get_date(date_today, ready_date):
    """
    forms the start and end date of the search
    :param date_today: today's date
    :param ready_date: desired period
    :return: search start and end date
    """
    start_date = None
    finish_date = None
    if ready_date == 'this_week':
        start_date = date_today - timedelta(
            days=datetime.today().weekday(), hours=date_today.hour,
            minutes=date_today.minute, seconds=date_today.second,
            microseconds=date_today.microsecond
        )
        finish_date = start_date + timedelta(days=7)

    elif ready_date == 'previous_week':
        finish_date = date_today - timedelta(
            days=datetime.today().weekday(), hours=date_today.hour,
            minutes=date_today.minute, seconds=date_today.second,
            microseconds=date_today.microsecond
        )
        start_date = finish_date - timedelta(days=7)

    elif ready_date == 'current_month':
        start_date = date_today.replace(
            month=date_today.month, day=1, hour=0, minute=0, second=0,
            microsecond=0
        )
        try:
            finish_date = start_date + relativedelta(
                month=date_today.month + 1
            )
        except calendar.IllegalMonthError:
            finish_date = start_date + timedelta(days=31)

    elif ready_date == 'previous_month':
        finish_date = date_today.replace(
            month=date_today.month, day=1, hour=0, minute=0, second=0,
            microsecond=0
        )
        start_date = finish_date - relativedelta(
            month=date_today.month - 1
        )
        if start_date == finish_date:
            start_date = finish_date - timedelta(days=31)

    elif ready_date == 'current_quarter':
        if date_today.month in range(1, 4):
            start_date = date_today.replace(
                month=1, day=1, hour=0, minute=0, second=0,
                microsecond=0
            )
            finish_date = date_today.replace(
                month=4, day=1, hour=0, minute=0, second=0,
                microsecond=0
            )

        elif date_today.month in range(4, 7):
            start_date = date_today.replace(
                month=4, day=1, hour=0, minute=0, second=0,
                microsecond=0
            )
            finish_date = date_today.replace(
                month=7, day=1, hour=0, minute=0, second=0,
                microsecond=0
            )

        elif date_today.month in range(7, 10):
            start_date = date_today.replace(
                month=7, day=1, hour=0, minute=0, second=0,
                microsecond=0
            )
            finish_date = date_today.replace(
                month=10, day=1, hour=0, minute=0, second=0,
                microsecond=0
            )

        else:
            start_date = date_today.replace(
                month=10, day=1, hour=0, minute=0, second=0,
                microsecond=0
            )
            finish_date = date_today.replace(
                year=date_today.year + 1, month=1, day=1, hour=0,
                minute=0, second=0, microsecond=0
            )

    elif ready_date == 'previous_quarter':
        if date_today.month in range(1, 4):
            start_date = date_today.replace(
                year=date_today.year - 1, month=10, day=1, hour=0,
                minute=0, second=0, microsecond=0
            )
            finish_date = date_today.replace(
                month=1, day=1, hour=0, minute=0, second=0,
                microsecond=0
            )

        elif date_today.month in range(3, 7):
            start_date = date_today.replace(
                month=1, day=1, hour=0, minute=0, second=0,
                microsecond=0
            )
            finish_date = date_today.replace(
                month=4, day=1, hour=0, minute=0, second=0,
                microsecond=0
            )

        elif date_today.month in range(6, 10):
            start_date = date_today.replace(
                month=4, day=1, hour=0, minute=0, second=0,
                microsecond=0
            )
            finish_date = date_today.replace(
                month=7, day=1, hour=0, minute=0, second=0,
                microsecond=0
            )

        else:
            start_date = date_today.replace(
                month=7, day=1, hour=0, minute=0, second=0,
                microsecond=0
            )
            finish_date = date_today.replace(
                month=10, day=1, hour=0, minute=0, second=0,
                microsecond=0
            )

    elif ready_date == 'this_year':
        start_date = date_today.replace(
            month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        finish_date = start_date + relativedelta(year=date_today.year + 1)

    elif ready_date == 'last_year':
        finish_date = date_today.replace(
            month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        start_date = finish_date - relativedelta(year=date_today.year - 1)

    return start_date, finish_date
