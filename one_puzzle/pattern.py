# -*- coding: utf-8 -*-
from operator import add, sub

from one_puzzle.element import Block


# 每个图案有八种形态，上下左右
# 旋转90度之后，上下左右
class OperateEntity(object):
    icon = "#"
    color = "#ffecb3"
    # 水平线
    horizontal_line = 0.5
    # 垂直线
    vertical_line = 2.5
    operates = []
    vertical_transfer = False
    horizontal_transfer = False
    rotate_transfer = False

    vertical_add = add
    horizontal_add = add
    vertical_sub = sub
    horizontal_sub = sub

    def __init__(self, col_offset=0, row_offset=0):
        self.col_offset = col_offset
        self.row_offset = row_offset
        self.horizontal_line += col_offset
        self.vertical_line += row_offset

    def vertical(self):
        self.vertical_transfer = not self.vertical_transfer
        self.vertical_sub, self.vertical_add = self.vertical_add, self.vertical_sub
        return self

    def horizontal(self):
        self.horizontal_transfer = not self.horizontal_transfer
        self.horizontal_sub, self.horizontal_add = self.horizontal_add, self.horizontal_sub
        return self

    @property
    def blocks(self):
        return [Block(x(self.horizontal_line), y(self.vertical_line), self) for x, y in self.operates]

    def __repr__(self):
        base = "{}({}, {})".format(self.__class__.__name__, self.col_offset, self.row_offset)
        if self.horizontal_transfer:
            base += ".horizontal()"
        if self.vertical_transfer:
            base += ".vertical()"
        if self.rotate_transfer:
            base += ".rotate()"
        return base

    def rotate(self):
        self.rotate_transfer = not self.rotate_transfer
        self.horizontal_line, self.vertical_line = self.vertical_line, self.horizontal_line
        for operate in self.operates:
            operate[0], operate[1] = operate[1], operate[0]
        return self


# 大 L
class BigLEntity(OperateEntity):
    icon = "+"
    # 水平线
    horizontal_line = 2.5
    # 垂直线
    vertical_line = 1.5
    color = "#d50000"

    def __init__(self, *args, **kwargs):
        super(BigLEntity, self).__init__(*args, **kwargs)

        self.operates = [
            [lambda x: self.horizontal_sub(x, 1.5), lambda y: self.vertical_sub(y, 0.5)],
            [lambda x: self.horizontal_sub(x, 0.5), lambda y: self.vertical_sub(y, 0.5)],
            [lambda x: self.horizontal_add(x, 0.5), lambda y: self.vertical_sub(y, 0.5)],
            [lambda x: self.horizontal_add(x, 1.5), lambda y: self.vertical_sub(y, 0.5)],
            [lambda x: self.horizontal_add(x, 1.5), lambda y: self.vertical_add(y, 0.5)],
        ]


# 满方块
class FullSmashEntity(OperateEntity):
    icon = "@"
    color = "#e65100"
    # 水平线
    horizontal_line = 1.5
    # 垂直线
    vertical_line = 2

    def __init__(self, *args, **kwargs):
        super(FullSmashEntity, self).__init__(*args, **kwargs)

        self.operates = [
            [lambda x: self.horizontal_sub(x, 0.5), lambda y: self.vertical_sub(y, 1)],
            [lambda x: self.horizontal_add(x, 0.5), lambda y: self.vertical_sub(y, 1)],
            [lambda x: self.horizontal_sub(x, 0.5), lambda y: self.vertical_add(y, 0)],
            [lambda x: self.horizontal_add(x, 0.5), lambda y: self.vertical_add(y, 0)],
            [lambda x: self.horizontal_sub(x, 0.5), lambda y: self.vertical_add(y, 1)],
            [lambda x: self.horizontal_add(x, 0.5), lambda y: self.vertical_add(y, 1)],
        ]


# 缺口方块
class LackSmashEntity(FullSmashEntity):
    icon = "#"
    color = "#2e7d32"

    def __init__(self, *args, **kwargs):
        super(LackSmashEntity, self).__init__(*args, **kwargs)
        self.operates.pop()


# 大 Z
class BigZEntity(OperateEntity):
    icon = "$"
    color = "#c94ed1"
    # 水平线
    horizontal_line = 2
    # 垂直线
    vertical_line = 2

    def __init__(self, *args, **kwargs):
        super(BigZEntity, self).__init__(*args, **kwargs)

        self.operates = [
            [lambda x: self.horizontal_sub(x, 1), lambda y: self.vertical_sub(y, 1)],
            [lambda x: self.horizontal_sub(x, 1), lambda y: self.vertical_sub(y, 0)],
            [lambda x: self.horizontal_add(x, 0), lambda y: self.vertical_add(y, 0)],
            [lambda x: self.horizontal_add(x, 1), lambda y: self.vertical_add(y, 0)],
            [lambda x: self.horizontal_add(x, 1), lambda y: self.vertical_add(y, 1)],
        ]


# 凹
class SunkenEntity(OperateEntity):
    icon = "%"
    color = "#536dfe"
    # 水平线
    horizontal_line = 1.5
    # 垂直线
    vertical_line = 2

    def __init__(self, *args, **kwargs):
        super(SunkenEntity, self).__init__(*args, **kwargs)

        self.operates = [
            [lambda x: self.horizontal_sub(x, 0.5), lambda y: self.vertical_sub(y, 1)],
            [lambda x: self.horizontal_add(x, 0.5), lambda y: self.vertical_sub(y, 1)],
            [lambda x: self.horizontal_add(x, 0.5), lambda y: self.vertical_add(y, 0)],
            [lambda x: self.horizontal_sub(x, 0.5), lambda y: self.vertical_add(y, 1)],
            [lambda x: self.horizontal_add(x, 0.5), lambda y: self.vertical_add(y, 1)],
        ]


# 凸
class ConvexEntity(OperateEntity):
    icon = "&"
    color = "#00897b"
    # 水平线
    horizontal_line = 1.5
    # 垂直线
    vertical_line = 2.5

    def __init__(self, *args, **kwargs):
        super(ConvexEntity, self).__init__(*args, **kwargs)

        self.operates = [
            [lambda x: self.horizontal_add(x, 0.5), lambda y: self.vertical_sub(y, 1.5)],
            [lambda x: self.horizontal_sub(x, 0.5), lambda y: self.vertical_sub(y, 0.5)],
            [lambda x: self.horizontal_add(x, 0.5), lambda y: self.vertical_sub(y, 0.5)],
            [lambda x: self.horizontal_add(x, 0.5), lambda y: self.vertical_add(y, 0.5)],
            [lambda x: self.horizontal_add(x, 0.5), lambda y: self.vertical_add(y, 1.5)],
        ]


# 等边L
class EquilateralLEntity(OperateEntity):
    icon = "*"
    color = "#1976d2"
    # 水平线
    horizontal_line = 2
    # 垂直线
    vertical_line = 2

    def __init__(self, *args, **kwargs):
        super(EquilateralLEntity, self).__init__(*args, **kwargs)
        self.operates = [
            [lambda x: self.horizontal_sub(x, 1), lambda y: self.vertical_sub(y, 1)],
            [lambda x: self.horizontal_sub(x, 0), lambda y: self.vertical_sub(y, 1)],
            [lambda x: self.horizontal_add(x, 1), lambda y: self.vertical_sub(y, 1)],
            [lambda x: self.horizontal_add(x, 1), lambda y: self.vertical_add(y, 0)],
            [lambda x: self.horizontal_add(x, 1), lambda y: self.vertical_add(y, 1)],
        ]


# 剑，闪电
class StilettoEntity(OperateEntity):
    icon = "^"
    color = "#6200ea"
    # 水平线
    horizontal_line = 2.5
    # 垂直线
    vertical_line = 1.5

    def __init__(self, *args, **kwargs):
        super(StilettoEntity, self).__init__(*args, **kwargs)

        self.operates = [
            [lambda x: self.horizontal_sub(x, 1.5), lambda y: self.vertical_sub(y, 0.5)],
            [lambda x: self.horizontal_sub(x, 0.5), lambda y: self.vertical_sub(y, 0.5)],
            [lambda x: self.horizontal_sub(x, 0.5), lambda y: self.vertical_add(y, 0.5)],
            [lambda x: self.horizontal_add(x, 0.5), lambda y: self.vertical_add(y, 0.5)],
            [lambda x: self.horizontal_add(x, 1.5), lambda y: self.vertical_add(y, 0.5)],
        ]


total_entity_classes = [
    BigLEntity,
    BigZEntity,
    LackSmashEntity,
    FullSmashEntity,
    EquilateralLEntity,
    StilettoEntity,
    ConvexEntity,
    SunkenEntity,
]
