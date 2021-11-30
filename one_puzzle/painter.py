# -*- coding: utf-8 -*-
import sys
import typing
from abc import ABCMeta, abstractmethod

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
import rich
from rich.box import Box
from rich.columns import Columns
from rich.panel import Panel
from rich.style import Style

from one_puzzle import __name__
from one_puzzle.pattern import OperateEntity
from one_puzzle.element import (
    Block,
    TARGET_COLOR,
    CALENDAR_PUZZLE_COLUMN,
    total_months,
    total_days,
)

total_blocks = total_months + total_days
total_blocks_map = {(block.row, block.col): block for block in total_blocks}


class Painter(metaclass=ABCMeta):
    @abstractmethod
    def draw_target(self, month_block, day_block):
        raise NotImplementedError

    @abstractmethod
    def show(self, success_entities=None):
        raise NotImplementedError


class QtPainter(Painter):
    def __init__(self, width=600, height=600):
        self.width = width
        self.height = height
        self.column = CALENDAR_PUZZLE_COLUMN

        self.app = QApplication(sys.argv)
        self.widget = QWidget()
        self.widget.setWindowTitle(__name__)
        self.widget.resize(width, height)

        self.block_width = 0.95 * (width / self.column)
        self.block_interval = 0.05 * width / (self.column + 1)

    def draw_block(self, column_num, row_num, color="cyan", text=None):

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

    def draw_pattern(self, pattern):
        # type: (OperateEntity) -> ()
        for block in pattern.blocks:
            self.draw_block(block.col, block.row, pattern.color)

    def draw_target(self, month_block, day_block):
        # type: (Block, Block) -> None
        self.draw_block(month_block.col, month_block.row, TARGET_COLOR, month_block.__class__.__name__.title())
        self.draw_block(day_block.col, day_block.row, TARGET_COLOR, str(day_block.index))

    def show(self, success_entities=None):

        for entity, entity_blocks in success_entities.items():
            for entity_block in entity_blocks:
                self.draw_block(entity_block.col, entity_block.row, entity.color)

        self.widget.show()
        self.app.exec_()


class CliPainter(Painter):
    def __init__(self):
        self.column = CALENDAR_PUZZLE_COLUMN

    def show(self, success_entities=None):
        blocks = []  # type: typing.List[Block]

        for entity, entity_blocks in success_entities.items():
            blocks.extend(entity_blocks)

        block_map = {}
        for block in blocks:
            block_map[(block.row, block.col)] = block

        for i in range(self.column):
            for j in range(self.column):
                block = block_map.get((i + 1, j + 1))
                if not block:
                    print("   ", end="")
                else:
                    print(" {} ".format(block.entity.icon), end="")
            print()

    def draw_target(self, month_block, day_block):
        pass


class RichPainter(Painter):
    def __init__(self):
        self.column = CALENDAR_PUZZLE_COLUMN
        self.console = rich.get_console()
        self.month_block = self.day_block = None

    def show(self, success_entities=None):
        blocks = []  # type: typing.List[Block]

        for entity, entity_blocks in success_entities.items():
            blocks.extend(entity_blocks)

        block_map = {}
        for block in blocks:
            block_map[(block.row, block.col)] = block

        for i in range(self.column):
            panels = []
            for j in range(self.column):
                block = block_map.get((i + 1, j + 1))
                block_index = total_blocks_map.get((i + 1, j + 1))

                if not block:
                    if not block_index:
                        continue
                    panels.append(
                        Panel(
                            " {}".format(
                                block_index.index if block_index.index else block_index.__class__.__name__.title()
                            ),
                            width=7,
                            box=Box("    \n" * 8),
                            padding=0,
                            style=Style(bgcolor='white'),
                        )
                    )

                else:
                    panels.append(
                        Panel(
                            " {}".format(
                                block_index.index if block_index.index else block_index.__class__.__name__.title()
                            ),
                            width=7,
                            padding=0,
                            box=Box("    \n" * 8),
                            style=Style(bgcolor=block.entity.color),
                        )
                    )
            self.console.print(Columns(panels))
            self.console.print("", new_line_start=True)

    def draw_target(self, month_block, day_block):
        self.month_block = month_block
        self.day_block = day_block
