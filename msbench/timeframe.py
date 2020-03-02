# -*- coding:utf-8 -*-


# TODO: "4H" has some issues and variable length records cannot be written.
# default_timeframes = "1Sec,10Sec,30Sec,1Min,5Min,15Min,30Min,1H,2H,4H,1D"
default_timeframes = "1Sec,10Sec,30Sec,1Min,5Min,15Min,30Min,1H,2H,1D"
valid_timeframes = {"1Sec", "10Sec", "30Sec", "1Min", "5Min", "15Min", "30Min", "1H", "2H", "1D"}


def is_valid_timeframe(s: str) -> bool:
    return s in valid_timeframes
