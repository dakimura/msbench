# -*- coding:utf-8 -*-

import time
from datetime import datetime
from datetime import timedelta
from random import randrange

import numpy as np
import pymarketstore as pymkts

from msbench.limit import get_limit
from msbench.time_range import get_range

# dd/mm/yyyy hh:mm:ss format
strtime_format = "%d/%m/%Y %H:%M:%S"


class MarketStoreClient:
    def __init__(self, host: str = "localhost:5993", grpc_host: str = "localhost:5995"):
        self.host = host
        self.cli = pymkts.Client(endpoint="http://{}/rpc".format(host))
        self.grpc_cli = pymkts.Client(endpoint=grpc_host, grpc=True)

    def random_query(self, symbol: str, timeframe: str, attribute_group: str, size: int, num: int,
                     limit_from_start: bool,
                     time_range: str, limit: str, grpc: bool) -> int:
        if num <= 0:
            return 0

        params = []
        for k in range(num):
            start, end = get_range(time_range)
            params.append(
                pymkts.Param(symbols=symbol, timeframe=timeframe, attrgroup=attribute_group, start=start, end=end,
                             limit=get_limit(limit, size), limit_from_start=limit_from_start))

        c = self.get_client(grpc)

        # first query takes a lot of time compared to the following queries.
        # query once to remove the effect.
        if num > 0:
            c.query(params=params[0])


        now = time.time_ns()
        for k in range(num):
            c.query(params=params[k])
            # reply = self.cli.query(params[k])
            # print(reply.first().df())
        elapsed = time.time_ns() - now

        return elapsed

    def random_write(self, symbol: str, timeframe: str, attribute_group: str,
                     size: int, num: int, is_variable_length: bool, record_size: int, grpc: bool) -> int:

        """
        write specified size of random records, specified times.


        - data are in a year.
        - data schema is "Ask(f4), Bid(f4), Nanoseconds(f4)

        :param symbol:
        :param timeframe:
        :param attribute_group:
        :param num:
        :param is_variable_length:
        :param record_size:
        :param grpc:
        :return:
        """
        if num <= 0:
            return 0

        bucket = "{}/{}/{}".format(symbol, timeframe, attribute_group)

        # # 1 column(data type:i8) = 8 byte
        # e.g. record_size = 32 = 4 * 8 byte
        # Epoch (required): 8byte
        # Nanoseconds (required for variable_length bucket): 4 byte, but will be padded to 8byte
        # column0, column1, ... column((record_size/8)-2): record_size - 16 byte
        # 8 + 8 + record_size - 16 = record_size byte
        data_type = [('Epoch', 'i8')]
        data_type.extend([('Column{}'.format(k), 'i8') for k in range(int(record_size / 8) - 2)])
        data_type.append(('Nanoseconds', 'i4'))

        dates = []
        for k in range(size):
            dates.append(random_date(start=datetime.strptime("01/01/2019 00:00:00", strtime_format),
                                     end=datetime.strptime("01/01/2020 00:00:00", strtime_format)))

        # sort datetimes as the data written to marketstore are usually time-series
        # and written in the ascending order of time
        dates.sort()

        data = []
        for k in range(size):
            recarray = [0 for t in range(int(record_size/8))]
            recarray[0] = int(dates[k].timestamp())
            for t in range(1, int(record_size/8)):
                recarray[t] = random_int()
            data.append(np.array([tuple(recarray)], dtype=data_type))

        # data = np.array([(pd.Timestamp('2017-01-01 00:00').value / 10 ** 9, 10.0)],
        #                 dtype=[('Epoch', 'i8'), ('Ask', 'f4')])
        # cli.write(data, 'TEST/1Min/Tick')

        c = self.get_client(grpc)

        now = time.time_ns()
        for k in range(num):
            for record in data:
                c.write(record, bucket, isvariablelength=is_variable_length)

        elapsed = time.time_ns() - now
        return elapsed

    def destroy(self, tbk: str, grpc: bool) -> int:
        c = self.get_client(grpc)
        return c.destroy(tbk=tbk)

    def get_client(self, grpc: bool):
        if grpc:
            return self.grpc_cli
        else:
            return self.cli


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


if __name__ == "__main__":
    mscli = MarketStoreClient()
    # mscli.random_query(symbol="DEBUG2", timeframe="1Sec", attribute_group="TICK", num=100)
    mscli.random_write_varlen_data(symbol="DEBUG2", timeframe="1Sec", attribute_group="TICK", size=10, num=4)
