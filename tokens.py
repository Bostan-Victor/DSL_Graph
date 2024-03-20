from enum import Enum
from dataclasses import dataclass


class TokenType(Enum):
    DASH = 0
    NAME = 1
    LEFT = 2
    RIGHT = 3
    FINAL = 4
    WEIGHT = 5


@dataclass
class Token:
    type: TokenType
    value: any = None

    def __repr__(self):
        return self.type.name + (f":{self.value}" if self.value is not None else "")
