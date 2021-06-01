from enum import Enum


class DatabaseResult(Enum):
    FAILURE = 1
    DONT_EXIST = 2
    SUCCESS = 3
