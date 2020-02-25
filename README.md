# msbench
A benchmarking tool for [marketstore](https://github.com/alpacahq/marketstore).


## Usage

```
$ pip install msbench
$ msbench -h
usage: msbench [-h] [--host HOST] [--size SIZE] [--write-num WRITE_NUM]
               [--query-num QUERY_NUM]

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           marketstore server host(e.g. 'localhost:5993')
  --size SIZE           data size to write/query. default is 100.
  --write-num WRITE_NUM
                        the number of trials to write. default is 1.
  --query-num QUERY_NUM
                        the number of trials to query. default is 10.
                        
$ msbench --host localhost:5993
timeframe, data_size, elapsed_time_per_operation(write/query)
[is_variable_length=False, data_size=100]
1Sec   24.38286ms/write
10Sec  23.84164ms/write
30Sec  23.94453ms/write
1Min   23.52767ms/write
5Min   23.88158ms/write
15Min  23.23138ms/write
30Min  23.91732ms/write
1H     24.05618ms/write
2H     32.43575ms/write
1D     24.11660ms/write
1Sec   38.74770ms/query
10Sec  9.66140ms/query
30Sec  2.98230ms/query
1Min   2.75860ms/query
5Min   1.86090ms/query
15Min  1.51900ms/query
30Min  1.59630ms/query
1H     1.64530ms/query
2H     1.46650ms/query
1D     1.60340ms/query
[is_variable_length=True, data_size=100]
1Sec   24.62127ms/write
10Sec  24.26307ms/write
30Sec  24.88134ms/write
1Min   24.71942ms/write
5Min   23.48047ms/write
15Min  23.94907ms/write
30Min  24.64881ms/write
1H     23.25042ms/write
2H     28.69883ms/write
1D     28.24308ms/write
1Sec   50.30020ms/query
10Sec  4.06780ms/query
30Sec  3.47400ms/query
1Min   2.32680ms/query
5Min   2.01010ms/query
15Min  2.12670ms/query
30Min  2.46700ms/query
1H     1.91930ms/query
2H     2.00120ms/query
1D     1.60810ms/query
```

Because the data file structure of marketstore depends on the timeframe (e.g. "1D", "10Sec", ...),
This tool calculates the write/query performance for each of them.



## Notes
- tested by python3.7.2