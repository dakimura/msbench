# msbench
A benchmarking tool for [marketstore](https://github.com/alpacahq/marketstore).


## Usage

```
$ pip install msbench
$ msbench -h
usage: msbench [-h] [--host HOST] [--size SIZE] [--write-num WRITE_NUM]
               [--query-num QUERY_NUM] [--timeframes TIMEFRAMES]
               [--limit LIMIT] [--limit-from-start LIMIT_FROM_START]
               [--range RANGE] [--grpc GRPC] [--grpc-host GRPC_HOST]
               [--record-size RECORD_SIZE] [--format FORMAT]
               [--target-bucket TARGET_BUCKET]

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           marketstore server host(e.g. 'localhost:5993')
  --size SIZE           data size to write/query. default is 100.
  --write-num WRITE_NUM
                        the number of trials to write. default is 1.
  --query-num QUERY_NUM
                        the number of trials to query. default is 10.
  --timeframes TIMEFRAMES
                        comma-separated timeframes to benchmark. default is
                        1Sec,10Sec,30Sec,1Min,5Min,15Min,30Min,1H,2H,1D
  --limit LIMIT         maximum number of data to query. default is None(=no
                        limit)
  --limit-from-start LIMIT_FROM_START
                        'true', 'false', or 'random'.when true, limit the
                        query range in the ascending order.
  --range RANGE         timerange to query. '1year' or 'random'. default
                        is'1year'.
  --grpc GRPC           when specified, GRPC api is used.
  --grpc-host GRPC_HOST
                        marketstore server host for GRPC
                        API(default='localhost:5995'). When --grpc=true, The
                        default value is used unless this param is specified.
  --record-size RECORD_SIZE
                        record size in byte. default is 32[byte](=4 * 8byte
                        column). This value should be multiples of 8, and
                        between 16 and 128.
  --format FORMAT       result is put in comma-separated string when 'csv' or
                        'csv-noheader' is specified.when 'csv-noheader' is
                        specified, first line(=column names) is omitted.
  --target-bucket TARGET_BUCKET
                        
$ msbench --host=localhost:5995 --grpc=True --size=100 --write-num=1 --query-num=10 --limit-from-start=true
timeframe, elapsed_time_per_operation(write/query)
[is_variable_length=False, data_size=100]
1Min   13.59064ms/write
30Sec  13.82150ms/write
10Sec  14.00641ms/write
2H     12.76107ms/write
1D     12.78084ms/write
30Min  13.03739ms/write
5Min   12.76048ms/write
1H     12.41011ms/write
15Min  12.90770ms/write
1Sec   18.46394ms/write
1Min   3.72280ms/query
30Sec  6.37370ms/query
10Sec  18.16850ms/query
2H     0.59140ms/query
1D     0.43410ms/query
30Min  0.95510ms/query
5Min   1.03330ms/query
1H     0.49650ms/query
15Min  0.70810ms/query
1Sec   216.13390ms/query
[is_variable_length=True, data_size=100]
1Min   13.39669ms/write
30Sec  13.42967ms/write
10Sec  13.50055ms/write
2H     12.91233ms/write
1D     12.73356ms/write
30Min  13.19201ms/write
5Min   13.20497ms/write
1H     12.85881ms/write
15Min  13.17280ms/write
1Sec   13.60641ms/write
1Min   3.57570ms/query
30Sec  5.05980ms/query
10Sec  16.35210ms/query
2H     0.64120ms/query
1D     0.53300ms/query
30Min  0.66760ms/query
5Min   1.03000ms/query
1H     0.68940ms/query
15Min  1.25760ms/query
1Sec   178.23130ms/query
```

Because the data file structure of marketstore depends on the timeframe (e.g. "1D", "10Sec", ...),
This tool calculates the write/query performance for each of them.



## Notes
- tested by python3.7.2