# -*- coding:utf-8 -*-

import logging
import sys
from argparse import ArgumentParser

from msbench.client import MarketStoreClient
from msbench.limit import default_limit, is_valid_limit
from msbench.limit_from_start import *
from msbench.time_range import default_range, is_valid_range
from msbench.timeframe import default_timeframes, is_valid_timeframe


def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('--host', type=str, default="localhost:5993",
                           help="marketstore server host(e.g. 'localhost:5993')")

    argparser.add_argument('--size', type=int, default=100,
                           help="data size to write/query. default is 100.")

    argparser.add_argument('--write-num', type=int, default=1,
                           help="the number of trials to write. default is 1.")

    argparser.add_argument('--query-num', type=int, default=10,
                           help="the number of trials to query. default is 10.")

    argparser.add_argument('--timeframes', type=str, default=default_timeframes,
                           help="comma-separated timeframes to benchmark. default is" + default_timeframes)

    argparser.add_argument('--limit', type=str, default=default_limit,
                           help="maximum number of data to query. default is None(=no limit)")

    argparser.add_argument('--limit-from-start', type=str, default=default_limit_from_start,
                           help="'true', 'false', or 'random'." +
                                "when true, limit the query range in the ascending order.")

    argparser.add_argument('--range', type=str, default=default_range,
                           help="timerange to query. '1year' or 'random'. default is'1year'.")

    # argparser.add_argument('-dlc', '--drawLearningCurve', type=bool,
    #                        default=False,
    #                        help='Whether to draw learning curve after learning')
    # argparser.add_argument('-po', '--predictOnly', type=bool,
    #                        default=False,
    #                        help='Only execute predict.')
    return argparser.parse_args()


def main():
    args = get_option()

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    cli = MarketStoreClient(host=args.host)

    size = args.size
    write_num = args.write_num
    query_num = args.query_num

    # validate timeframes
    timeframes = args.timeframes.split(",")
    if args.timeframes != default_timeframes:
        for tf in timeframes:
            if not is_valid_timeframe(tf):
                print("invalid timeframe {}".format(tf))
                sys.exit(1)
        # deduplicate timeframes just in case that users specify same timeframes
        timeframes = list(set(timeframes))

    # validate limit_from_start
    limit_from_start = args.limit_from_start
    if limit_from_start != default_limit_from_start:
        if not is_valid_limit_from_start(limit_from_start):
            print("invalid limit-from-start {}".format(limit_from_start))
            sys.exit(1)

    limit_from_start_bool = get_limit_from_start(limit_from_start)

    # validate range
    time_range = args.range
    if time_range != default_range:
        if not is_valid_range(time_range):
            print("invalid range {}".format(time_range))
            sys.exit(1)

    # validate limit
    limit = args.limit
    if limit != default_limit and not is_valid_limit(limit):
        print("invalid limit {}".format(limit))
        sys.exit(1)

    print("timeframe, elapsed_time_per_operation(write/query)")
    for is_variable_length in [False, True]:
        if is_variable_length:
            symbol_prefix = "BENCHV"
        else:
            symbol_prefix = "BENCH"

        # Write
        print("[is_variable_length={}, data_size={}]".format(is_variable_length, size))
        for k in range(len(timeframes)):
            elapsed_nanos = cli.random_write(symbol="{}{}".format(symbol_prefix, k),
                                             timeframe=timeframes[k],
                                             attribute_group="TICK",
                                             size=size, num=write_num,
                                             is_variable_length=is_variable_length)
            if write_num > 0:
                print("{:7}{:.5f}ms/write".format(timeframes[k], elapsed_nanos / 10 ** 6 / write_num / size, ))

        # Query
        for k in range(len(timeframes)):
            elapsed_nanos = cli.random_query(symbol="{}{}".format(symbol_prefix, k),
                                             timeframe=timeframes[k],
                                             attribute_group="TICK",
                                             size=size, num=query_num, limit_from_start=limit_from_start_bool,
                                             time_range=time_range, limit=limit)
            if query_num > 0:
                print("{:7}{:.5f}ms/query".format(timeframes[k], elapsed_nanos / 10 ** 6 / query_num, ))


if __name__ == "__main__":
    main()
