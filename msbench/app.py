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
                           help="comma-separated timeframes to benchmark. default is " + default_timeframes)

    argparser.add_argument('--limit', type=str, default=default_limit,
                           help="maximum number of data to query. default is None(=no limit)")

    argparser.add_argument('--limit-from-start', type=str, default=default_limit_from_start,
                           help="'true', 'false', or 'random'." +
                                "when true, limit the query range in the ascending order.")

    argparser.add_argument('--range', type=str, default=default_range,
                           help="timerange to query. '1year' or 'random'. default is'1year'.")

    argparser.add_argument('--grpc', type=bool, default=False,
                           help="when specified, GRPC api is used.")

    argparser.add_argument('--grpc-host', type=str, default="localhost:5995",
                           help="marketstore server host for GRPC API(default='localhost:5995'). "
                                + "When --grpc=true, The default value is used unless this param is specified.")

    argparser.add_argument('--record-size', type=int, default=32,
                           help="record size in byte. default is 32[byte](=4 * 8byte column). " +
                                "This value should be multiples of 8, and between 16 and 128.")

    argparser.add_argument('--format', type=str, default="default",
                           help="result is put in comma-separated string when 'csv' or 'csv-noheader' is specified."
                                + "when 'csv-noheader' is specified, first line(=column names) is omitted.")

    argparser.add_argument('--target-bucket', type=str, default="")

    # argparser.add_argument('-dlc', '--drawLearningCurve', type=bool,
    #                        default=False,
    #                        help='Whether to draw learning curve after learning')
    # argparser.add_argument('-po', '--predictOnly', type=bool,
    #                        default=False,
    #                        help='Only execute predict.')
    return argparser.parse_args()


def validate_args(args):
    # validate timeframes
    timeframes = args.timeframes.split(",")
    if args.timeframes != default_timeframes:
        for tf in timeframes:
            if not is_valid_timeframe(tf):
                print("invalid timeframe {}".format(tf))
                sys.exit(1)

    # validate limit_from_start
    limit_from_start = args.limit_from_start
    if limit_from_start != default_limit_from_start:
        if not is_valid_limit_from_start(limit_from_start):
            print("invalid limit-from-start {}".format(limit_from_start))
            sys.exit(1)

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

    # validate record size
    record_size = args.record_size
    if record_size < 16 or record_size > 128 or record_size % 8 != 0:
        print("--record_size should be multiples of 8, and between 16 and 128.")
        sys.exit(1)

    format = args.format
    if format not in ["default", "csv", "csv-noheader"]:
        print("only 'default', 'csv', and 'csv-noheader' is supported for --format arg.")
        sys.exit(1)


def main():
    args = get_option()
    validate_args(args)

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    cli = MarketStoreClient(host=args.host, grpc_host=args.grpc_host)

    size = args.size
    write_num = args.write_num
    query_num = args.query_num
    grpc = args.grpc
    record_size = args.record_size
    # deduplicate timeframes just in case that users specify same timeframes
    timeframes = list(set(args.timeframes.split(",")))
    limit_from_start = args.limit_from_start
    limit_from_start_bool = get_limit_from_start(limit_from_start)
    time_range = args.range
    limit = args.limit
    format = args.format

    if format == "csv":
        print(
            "is_variable_length,grpc,data_size,record_size,timeframe,operation(write/query),elapsed_time(ms/operation)")
    elif format == "default":
        print("timeframe, elapsed_time_per_operation(write/query)")

    for is_variable_length in [False, True]:
        if is_variable_length:
            symbol_prefix = "BENCHV"
        else:
            symbol_prefix = "BENCH"

        # Destroy (setup)
        for k in range(len(timeframes)):
            cli.destroy(tbk=get_bucket_name(symbol=symbol_prefix, timeframe=timeframes[k], attr_group="TICK"),
                        grpc=grpc)

        # Write
        if format == "default":
            print("[is_variable_length={}, data_size={}]".format(is_variable_length, size))
        for k in range(len(timeframes)):
            elapsed_nanos = cli.random_write(symbol="{}".format(symbol_prefix),
                                             timeframe=timeframes[k],
                                             attribute_group="TICK",
                                             size=size, num=write_num,
                                             is_variable_length=is_variable_length, record_size=record_size, grpc=grpc)
            if write_num > 0:
                if format in ["csv", "csv-noheader"]:
                    print_result(is_variable_length, grpc, size, record_size, timeframes[k], "write",
                                 "{}".format(elapsed_nanos / 10 ** 6 / write_num / size))
                else:
                    print("{:7}{:.5f}ms/write".format(timeframes[k], elapsed_nanos / 10 ** 6 / write_num / size, ))

        # Query
        for k in range(len(timeframes)):
            elapsed_nanos = cli.random_query(symbol="{}".format(symbol_prefix),
                                             timeframe=timeframes[k],
                                             attribute_group="TICK",
                                             size=size, num=query_num, limit_from_start=limit_from_start_bool,
                                             time_range=time_range, limit=limit, grpc=grpc)
            if query_num > 0:
                if format in ["csv", "csv-noheader"]:
                    print_result(is_variable_length, grpc, size, record_size, timeframes[k], "query",
                                 "{}".format(elapsed_nanos / 10 ** 6 / query_num))
                else:
                    print("{:7}{:.5f}ms/query".format(timeframes[k], elapsed_nanos / 10 ** 6 / query_num, ))

        # Destroy (tear down)
        # for k in range(len(timeframes)):
        #     # print("destroy {}".format(get_bucket_name(symbol=symbol_prefix, timeframe=timeframes[k], attr_group="TICK")))
        #     cli.destroy(tbk=get_bucket_name(symbol=symbol_prefix, timeframe=timeframes[k], attr_group="TICK"),
        #                 grpc=grpc)


def print_result(is_variable_length: bool, grpc: bool, size: int, record_size: int, timeframe: str, operation: str,
                 elapsed_time: str):
    print(",".join([str(is_variable_length), str(grpc), str(size), str(record_size), timeframe,
                    operation, elapsed_time]))


def get_bucket_name(symbol: str, timeframe: str, attr_group: str) -> str:
    return "{}/{}/{}".format(symbol, timeframe, attr_group)


if __name__ == "__main__":
    main()
