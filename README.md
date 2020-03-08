# msbench
A benchmarking tool for [marketstore](https://github.com/alpacahq/marketstore).


## Usage

```
$ pip install msbench
$ msbench -h
usage: msbench [-h] [--host HOST] [--size SIZE] [--write-num WRITE_NUM]
               [--query-num QUERY_NUM] [--timeframes TIMEFRAMES]
               [--limit LIMIT] [--limit-from-start LIMIT_FROM_START]
               [--range RANGE]

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           marketstore server host(e.g. 'localhost:5993')
  --size SIZE           data size to write/query. default is 100.
  --write-num WRITE_NUM
                        the number of trials to write. default is 1.
  --query-num QUERY_NUM
                        the number of trials to query. default is 10.
  --timeframes TIMEFRAMES
                        comma-separated timeframes to benchmark. default
                        is1Sec,10Sec,30Sec,1Min,5Min,15Min,30Min,1H,2H,1D
  --limit LIMIT         maximum number of data to query. default is None(=no
                        limit)
  --limit-from-start LIMIT_FROM_START
                        'true', 'false', or 'random'.when true, limit the
                        query range in the ascending order.
  --range RANGE         timerange to query. '1year' or 'random'. default
                        is'1year'.
                        
$ msbench --host=localhost:5993
timeframe, elapsed_time_per_operation(write/query)
[is_variable_length=False, data_size=100]
1Sec   26.38452ms/write
10Sec  25.36167ms/write
30Sec  26.40953ms/write
1Min   26.58795ms/write
5Min   26.32962ms/write
15Min  26.20697ms/write
30Min  26.13297ms/write
1H     26.46017ms/write
2H     33.60577ms/write
1D     25.83773ms/write
1Sec   189.34520ms/query
10Sec  20.15250ms/query
30Sec  8.17620ms/query
1Min   5.58030ms/query
5Min   3.13680ms/query
15Min  2.30740ms/query
30Min  2.19810ms/query
1H     1.91980ms/query
2H     1.59340ms/query
1D     1.66810ms/query
[is_variable_length=True, data_size=100]
1Sec   26.64488ms/write
10Sec  26.89350ms/write
30Sec  26.75442ms/write
1Min   26.72768ms/write
5Min   26.82692ms/write
15Min  25.99296ms/write
30Min  25.18656ms/write
1H     26.11412ms/write
2H     26.39308ms/write
1D     33.24013ms/write
1Sec   167.14670ms/query
10Sec  24.41130ms/query
30Sec  9.58960ms/query
1Min   6.57560ms/query
5Min   4.91310ms/query
15Min  3.41620ms/query
30Min  3.22180ms/query
1H     3.29080ms/query
2H     3.02750ms/query
1D     2.26990ms/query
```

Because the data file structure of marketstore depends on the timeframe (e.g. "1D", "10Sec", ...),
This tool calculates the write/query performance for each of them.



## Notes
- tested by python3.7.2