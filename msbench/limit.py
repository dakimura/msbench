# -*- coding:utf-8 -*-

import typing
from random import randrange

default_limit = ""


def is_valid_limit(s: str) -> bool:
    return s.lower() in {"", "random"}


def get_limit(s: str, size: int) -> typing.Optional[int]:
    ls = s.lower()
    if ls == "":
        return None
    elif ls == "random":
        return randrange(size)
    else:
        # default
        return None
