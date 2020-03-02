# -*- coding:utf-8 -*-

from enum import Enum
from random import randrange

default_limit_from_start = "random"


def is_valid_limit_from_start(s: str) -> bool:
    return s.lower() in {"true","false","random"}


def get_limit_from_start(s: str) -> bool:
    ls = s.lower()
    if ls == "true":
        return True
    elif ls == "false":
        return False
    elif ls == "random":
        return random_bool()
    else:
        # default
        return True


def random_bool():
    if randrange(2) == 1:
        return True
    else:
        return False
