# -*- coding: utf-8 -*-
import sys
from operator import add, sub

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

from one_puzzle import __name__
from one_puzzle.element import (
    JAN,
    FEB,
    MAR,
    MAY,
    APR,
    JUN,
    JUL,
    AUG,
    SEP,
    OCT,
    NOV,
    DEC,
    Block,
    MONTH_COLOR,
    DAY_COLOR,
)


class Board(object):
    def __init__(self, width=600, height=600, nox=False):
        self.width = width
        self.height = height
        self.column = 7
        self.nox = nox
        if not self.nox:
            self.app = QApplication(sys.argv)
            self.widget = QWidget()
            self.widget.setWindowTitle(__name__)
            self.widget.resize(width, height)

        self.block_width = 0.95 * (width / self.column)
        self.block_interval = 0.05 * width / (self.column + 1)

        self.months = [JAN(), FEB(), MAR(), APR(), MAY(), JUN(), JUL(), AUG(), SEP(), OCT(), NOV(), DEC()]
        self.days = [Block(3 + i // self.column, 1 + i % self.column) for i in range(31)]
        self.entities = []

    def draw_block(self, column_num, row_num, color="cyan", text=None):
        if self.nox:
            return

        w = QWidget(self.widget)
        w.setGeometry(
            int(column_num * self.block_interval + (column_num - 1) * self.block_width),
            int(row_num * self.block_interval + (row_num - 1) * self.block_width),
            int(self.block_width),
            int(self.block_width),
        )

        w.setStyleSheet('background-color:{}'.format(color))
        if text:
            text_label = QLabel(w)
            text_label.setStyleSheet('color:#ffffff')
            text_label.setText(text)
            text_label.setAlignment(Qt.AlignCenter)
            text_label.setFont(QFont('', 24))
            text_label.resize(self.block_width, self.block_width)

    def draw_months(self):
        for month in self.months:  # type: Block
            self.draw_block(month.col, month.row, MONTH_COLOR)

    def draw_days(self):
        for day in self.days:  # type: Block
            self.draw_block(day.col, day.row, DAY_COLOR)

    def draw_pattern(self, pattern):
        # type: (OperateEntity) -> ()
        for block in pattern.blocks:
            self.draw_block(block.col, block.row, pattern.color)

    def show(self, pattern=None):
        self.draw_months()
        self.draw_days()
        if pattern:
            self.draw_pattern(pattern)

        for entity in self.entities:
            self.draw_pattern(entity)

        if not self.nox:
            self.widget.show()
            self.app.exec_()

    def add_entity(self, entity):
        # type: (OperateEntity)->()
        self.entities.append(entity)


# 每个图案有八种形态，上下左右
# 旋转90度之后，上下左右
class OperateEntity(object):
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
        return [Block(x(self.horizontal_line), y(self.vertical_line)) for x, y in self.operates]

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
    color = "#2e7d32"

    def __init__(self, *args, **kwargs):
        super(LackSmashEntity, self).__init__(*args, **kwargs)
        self.operates.pop()


# 大 Z
class BigZEntity(OperateEntity):
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
