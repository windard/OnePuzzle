# -*- coding: utf-8 -*-

MONTH_COLOR = "#c1c1c1"
DAY_COLOR = "#c6c6c6"
TARGET_COLOR = "#212121"
CALENDAR_PUZZLE_COLUMN = 7


class Block(object):
    row = 1
    col = 1

    def __init__(self, row=None, col=None, entity=None, index=None):
        if row:
            self.row = int(row)

        if col:
            self.col = int(col)

        self.entity = entity
        self.index = index

    def __repr__(self):
        return "Block({}, {})".format(self.row, self.col)

    __str__ = __repr__

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return int("{}{}".format(self.row, self.col))


class JAN(Block):
    row = 1
    col = 1


class FEB(Block):
    row = 1
    col = 2


class MAR(Block):
    row = 1
    col = 3


class APR(Block):
    row = 1
    col = 4


class MAY(Block):
    row = 1
    col = 5


class JUN(Block):
    row = 1
    col = 6


class JUL(Block):
    row = 2
    col = 1


class AUG(Block):
    row = 2
    col = 2


class SEP(Block):
    row = 2
    col = 3


class OCT(Block):
    row = 2
    col = 4


class NOV(Block):
    row = 2
    col = 5


class DEC(Block):
    row = 2
    col = 6


total_months = [JAN(), FEB(), MAR(), APR(), MAY(), JUN(), JUL(), AUG(), SEP(), OCT(), NOV(), DEC()]
total_days = [
    Block(3 + (i // CALENDAR_PUZZLE_COLUMN), 1 + (i % CALENDAR_PUZZLE_COLUMN), index=i + 1) for i in range(31)
]
