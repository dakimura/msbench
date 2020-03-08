# -*- coding:utf-8 -*-

from datetime import datetime
from datetime import timedelta
from random import randrange

# dd/mm/yyyy hh:mm:ss format
strtime_format = "%d/%m/%Y %H:%M:%S"

default_range = "1year"
default_start = datetime.strptime("01/01/2019 00:00:00", strtime_format)
default_end = datetime.strptime("31/12/2019 23:59:59", strtime_format)


def is_valid_range(s: str) -> bool:
    return s.lower() in {"1year", "random"}


def get_range(s: str) -> (int, int):
    ls = s.lower()
    if ls == "1year":
        return default_start, default_end
    elif ls == "random":
        return random_range()
    else:
        # default
        return default_start, default_end


def random_range() -> (datetime, datetime):
    start = random_date(start=datetime.strptime("01/01/2019 00:00:00", strtime_format),
                        end=datetime.strptime("01/01/2020 00:00:00", strtime_format))
    end = random_date(start=datetime.strptime("01/01/2019 00:00:00", strtime_format),
                      end=datetime.strptime("01/01/2020 00:00:00", strtime_format))
    if start > end:
        start, end = end, start

    return start, end


def random_date(start, end) -> datetime:
    """
    This function will return a random datetime between two datetime
    objects.
    The precision is seconds.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)

    return start + timedelta(seconds=random_second)
