# -*- coding:utf-8 -*-

import time
from datetime import datetime
from datetime import timedelta
from random import randrange

import numpy as np
import pymarketstore as pymkts

# dd/mm/yyyy hh:mm:ss format
strtime_format = "%d/%m/%Y %H:%M:%S"


class MarketStoreClient:
    def __init__(self, host: str = "localhost:5993"):
        self.host = host
        self.cli = pymkts.Client(endpoint="http://{}/rpc".format(host))

    def random_query(self, symbol: str, timeframe: str, attribute_group: str, size: int, num: int) -> int:
        # TODO: add start, end, limit, limit_from_start options

        params = []
        for k in range(num):
            start = random_date(start=datetime.strptime("01/01/2019 00:00:00", strtime_format),
                                end=datetime.strptime("01/01/2020 00:00:00", strtime_format))
            end = random_date(start=datetime.strptime("01/01/2019 00:00:00", strtime_format),
                              end=datetime.strptime("01/01/2020 00:00:00", strtime_format))
            if start > end:
                start, end = end, start

            params.append(pymkts.Param(symbol, timeframe, attribute_group, start=start, end=end,
                                       limit=randrange(size), limit_from_start=random_bool()))

        now = time.time_ns()
        for k in range(num):
            self.cli.query(params[k])
            # reply = self.cli.query(params[k])
            # print(reply.first().df())
        elapsed = time.time_ns() - now

        return elapsed

    def random_write(self, symbol: str, timeframe: str, attribute_group: str,
                     size: int, num: int, is_variable_length: bool) -> int:

        """
        write specified size of random records, specified times.


        - data are in a year.
        - data schema is "Ask(f4), Bid(f4), Nanoseconds(f4)

        :param symbol:
        :param timeframe:
        :param attribute_group:
        :param num:
        :param is_variable_length:
        :return:
        """
        bucket = "{}/{}/{}".format(symbol, timeframe, attribute_group)
        data_type = [('Epoch', 'i8'), ('Bid', 'f4'), ('Ask', 'f4'), ('Nanoseconds', 'i4')]

        dates = []
        for k in range(size):
            dates.append(random_date(start=datetime.strptime("01/01/2019 00:00:00", strtime_format),
                                     end=datetime.strptime("01/01/2020 00:00:00", strtime_format)))

        # sort datetimes as the data written to marketstore are usually time-series
        # and written in the ascending order of time
        dates.sort()

        data = []
        for k in range(size):
            data.append(np.array([(int(dates[k].timestamp()),
                                   random_int(), random_int(), random_int())],
                                 dtype=data_type))

        now = time.time_ns()
        for k in range(num):
            for record in data:
                self.cli.write(record, bucket, isvariablelength=is_variable_length)

        elapsed = time.time_ns() - now
        return elapsed


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


def random_epoch(start: int, end: time) -> int:
    delta = end - start
    return start + randrange(delta)


def random_int():
    return randrange(1000000000)


def random_bool():
    if randrange(2) == 1:
        return True
    else:
        return False


if __name__ == "__main__":
    mscli = MarketStoreClient()
    # mscli.random_query(symbol="DEBUG2", timeframe="1Sec", attribute_group="TICK", num=100)
    mscli.random_write_varlen_data(symbol="DEBUG2", timeframe="1Sec", attribute_group="TICK", size=10, num=4)
