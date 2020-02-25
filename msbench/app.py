# -*- coding:utf-8 -*-

import logging
from argparse import ArgumentParser

from msbench.client import MarketStoreClient

# TODO: "4H" has some issues and variable length records cannot be written.
# timeframes = ["1Sec", "10Sec", "30Sec", "1Min", "5Min", "15Min", "30Min", "1H", "2H", "4H", "1D", ]
timeframes = ["1Sec", "10Sec", "30Sec", "1Min", "5Min", "15Min", "30Min", "1H", "2H", "1D", ]


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
            print("{:7}{:.5f}ms/write".format(timeframes[k], elapsed_nanos / 10 ** 6 / write_num / size, ))

        # Query
        for k in range(len(timeframes)):
            elapsed_nanos = cli.random_query(symbol="{}{}".format(symbol_prefix, k),
                                             timeframe=timeframes[k],
                                             attribute_group="TICK",
                                             size=size, num=query_num)
            print("{:7}{:.5f}ms/query".format(timeframes[k], elapsed_nanos / 10 ** 6 / query_num, ))


if __name__ == "__main__":
    main()
