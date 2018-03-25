from enum import Enum


class Moves(Enum):
    Up = "up",
    Down = "down",
    Left = "left",
    Right = "right",

    def __str__(self):
        return '%s' % self._value_
