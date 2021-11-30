# -*- coding: utf-8 -*-

import click
import random
import datetime

from queue import Queue
from collections import defaultdict
from typing import Set, Dict, List, Tuple, Type, Optional

from one_puzzle import __version__

from one_puzzle.painter import QtPainter, RichPainter, CliPainter, Painter
from one_puzzle.pattern import (
    OperateEntity,
    total_entity_classes,
)
from one_puzzle.element import (
    Block,
    total_months,
    total_days,
    CALENDAR_PUZZLE_COLUMN,
)


class Board(object):
    def __init__(self, width=600, height=600, style='qt'):
        self.width = width
        self.height = height
        self.column = CALENDAR_PUZZLE_COLUMN
        self.style = style
        self.painter = CliPainter()  # type: Painter
        if style == "qt":
            self.painter = QtPainter()
        elif style == "rich":
            self.painter = RichPainter()

        self.months = total_months.copy()
        self.days = total_days.copy()
        self.entities = []

        self.target_month = self.target_day = None

    def add_entity(self, entity):
        # type: (OperateEntity)->()
        self.entities.append(entity)

    def show(self, success_entities):
        self.painter.draw_target(self.target_month, self.target_day)
        self.painter.show(success_entities)


class Solver(object):
    def __init__(self, month=1, day=1, debug=False, get_all=False, nox=False, color=False):
        self.month = month
        self.day = day
        self.debug = debug
        self.get_all = get_all

        if not nox:
            self.board = Board()
        elif color:
            self.board = Board(style='rich')
        else:
            self.board = Board(style='cli')

        month_block = self.board.months[self.month - 1]
        day_block = self.board.days[self.day - 1]

        self.board.target_month = month_block
        self.board.target_day = day_block
        self.board.months.remove(month_block)
        self.board.days.remove(day_block)

    @classmethod
    def get_around(cls, block):
        surrounds = set()
        surrounds.add(Block(block.row + 1, block.col))
        surrounds.add(Block(block.row - 1, block.col))
        surrounds.add(Block(block.row, block.col + 1))
        surrounds.add(Block(block.row, block.col - 1))
        return surrounds

    @classmethod
    def validate_trap(cls, blocks):
        # 校验有独立的一个空，两个空，三个空，四个空的场景
        if not blocks:
            return True

        blocks = list(blocks)
        groups = []
        queue = Queue()

        while blocks:
            group = []
            block = blocks.pop()
            group.append(block)
            queue.put(block)

            while not queue.empty():
                block = queue.get()
                surrounds = cls.get_around(block)
                exists = surrounds & set(blocks)
                for exist in exists:
                    group.append(exist)
                    queue.put(exist)
                    blocks.remove(exist)

            if len(group) < 5:
                return False
            groups.append(group)

        return True

    @staticmethod
    def get_available_entities(blocks, entity_classes):
        # type: (Set[Block], List[Type[OperateEntity]]) -> Dict[Type[OperateEntity], Set[Tuple[Block]]]
        result = defaultdict(set)
        for entity_class in entity_classes:
            for i in range(CALENDAR_PUZZLE_COLUMN):
                for j in range(CALENDAR_PUZZLE_COLUMN):

                    for m in [lambda x: x, lambda x: x.rotate()]:
                        for n in [lambda x: x, lambda x: x.horizontal()]:
                            for p in [lambda x: x, lambda x: x.vertical()]:
                                entity = entity_class(i, j)
                                entity = m(n(p(entity)))
                                # 全部都在剩余空位内
                                if set(entity.blocks) - blocks:
                                    continue

                                result[entity_class].add(tuple(sorted(entity.blocks, key=Block.__hash__)))
        return result

    def multi_solve(self, urandom=False):
        calculated = 0
        result = []
        totals = set(self.board.months + self.board.days)

        def traceback(available_entity_blocks, filled_entities, filled_entity_blocks):
            # type: (Dict[Type[OperateEntity], Set[Tuple[Block]]], Dict[Type[OperateEntity], Set[Block]], Set[Block]) -> Optional[Dict[Type[OperateEntity], Set[Block]]] # noqa
            if not available_entity_blocks:
                return

            nonlocal calculated
            calculated += 1

            entity_keys = list(available_entity_blocks.keys())
            if urandom:
                entity_class = random.choice(entity_keys)
            else:
                entity_class = entity_keys.pop()

            entity_class_groups = available_entity_blocks[entity_class]

            for entity_class_group in entity_class_groups:

                entity_class_group = set(entity_class_group)
                # 有重复
                if filled_entity_blocks & entity_class_group:
                    continue

                left_blocks = totals - filled_entity_blocks - entity_class_group
                # 有成功
                if not left_blocks:
                    # 有成功
                    if self.debug:
                        print(
                            "success in {:7}:{}".format(
                                calculated, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            )
                        )

                    filled_entities[entity_class] = entity_class_group
                    success_result = filled_entities.copy()
                    result.append(success_result)
                    if not self.get_all:
                        return success_result

                elif not self.validate_trap(left_blocks):
                    # 有空洞，此路不通，直接 continue
                    continue

                del available_entity_blocks[entity_class]
                filled_entities[entity_class] = entity_class_group
                # 继续下一个计算
                success_result = traceback(
                    available_entity_blocks, filled_entities, filled_entity_blocks | entity_class_group
                )
                if success_result:
                    return success_result

                del filled_entities[entity_class]
                available_entity_blocks[entity_class] = entity_class_groups

        if self.debug:
            print("start at:{}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        available_entities = self.get_available_entities(totals, total_entity_classes)
        success_entities = traceback(available_entities, dict(), set())

        if self.debug:
            print("end   at:{}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            print("calculated times:{}".format(calculated))
            print("success entities:{}".format(success_entities))

        if self.get_all:
            print("groups number:{}".format(len(result)))
            print("all success group:{}".format(result))
            success_entities = result[-1]

        self.board.show(success_entities)


@click.command()
@click.help_option("-h", "--help")
@click.version_option(__version__, '-v', '--version')
@click.argument('month', type=int)
@click.argument('day', type=int)
@click.option('-d', '--debug', is_flag=True, default=False, help='show debug message.')
@click.option('-a', '--all', 'get_all', is_flag=True, default=False, help='get all result.')
@click.option('-n', '--nox', is_flag=True, default=False, help='no screen show.')
@click.option('-c', '--color', is_flag=True, default=False, help='colorful cli show.')
@click.option('-r', '-u', '--urandom', is_flag=True, default=False, help='random calculate.')
def main(month, day, debug=False, get_all=False, nox=False, color=False, urandom=False):
    solver = Solver(month, day, debug, get_all, nox, color)
    solver.multi_solve(urandom)
