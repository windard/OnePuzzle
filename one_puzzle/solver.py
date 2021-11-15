# -*- coding: utf-8 -*-

import click
import random
import datetime

from queue import Queue
from collections import defaultdict
from typing import Set, Dict, List, Tuple, Type, Optional, Generic

from one_puzzle.element import (
    Block,
    TARGET_COLOR,
)
from one_puzzle.pattern import (
    Board,
    BigZEntity,
    BigLEntity,
    LackSmashEntity,
    FullSmashEntity,
    EquilateralLEntity,
    StilettoEntity,
    ConvexEntity,
    SunkenEntity,
    OperateEntity,
)


class Solver(object):
    def __init__(self, month=1, day=1, debug=False, get_all=False):
        self.month = month
        self.day = day
        self.entity_classes = [
            BigLEntity,
            BigZEntity,
            LackSmashEntity,
            FullSmashEntity,
            EquilateralLEntity,
            StilettoEntity,
            ConvexEntity,
            SunkenEntity,
        ]
        self.calculated = 0
        self.debug = debug
        self.get_all = get_all

    @staticmethod
    def get_around(block):
        surrounds = set()
        surrounds.add(Block(block.row + 1, block.col))
        surrounds.add(Block(block.row - 1, block.col))
        surrounds.add(Block(block.row, block.col + 1))
        surrounds.add(Block(block.row, block.col - 1))
        return surrounds

    def validate_trap(self, blocks):
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
                surrounds = self.get_around(block)
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
            for i in range(7):
                for j in range(7):

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

    def faster_solve(self, nox=False, urandom=False):
        board = Board(nox=nox)

        month_block = board.months[self.month - 1]
        day_block = board.days[self.day - 1]
        board.draw_block(month_block.col, month_block.row, TARGET_COLOR, month_block.__class__.__name__)
        board.draw_block(day_block.col, day_block.row, TARGET_COLOR, str(self.day))
        board.months.remove(month_block)
        board.days.remove(day_block)

        totals = set(board.months + board.days)

        result = []
        self.calculated = 0

        def traceback(available_entity_blocks, filled_entities, filled_entity_blocks):
            # type: (Dict[Type[OperateEntity], Set[Tuple[Block]]], Dict[Type[OperateEntity], Set[Block]], Set[Block]) -> Optional[Dict[Type[OperateEntity], Set[Block]]] # noqa
            if not available_entity_blocks:
                return

            self.calculated += 1

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
                                self.calculated, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

        available_entities = self.get_available_entities(totals, self.entity_classes)
        success_entities = traceback(available_entities, {}, set())

        if self.debug:
            print("end   at:{}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            print("calculated times:{}".format(self.calculated))
            print("success entities:{}".format(success_entities))

        if self.get_all:
            print("groups number:{}".format(len(result)))
            print("all success group:{}".format(result))
            success_entities = result[-1]

        for entity, entity_blocks in success_entities.items():
            for entity_block in entity_blocks:
                board.draw_block(entity_block.col, entity_block.row, entity.color)
        board.show(skip_blocks=True)


@click.command()
@click.help_option("-h", "--help")
@click.argument('month', type=int)
@click.argument('day', type=int)
@click.option('-d', '--debug', is_flag=True, default=False, help='show debug message.')
@click.option('-a', '--all', 'get_all', is_flag=True, default=False, help='get all result.')
@click.option('-n', '--nox', is_flag=True, default=False, help='no screen show.')
@click.option('-r', '-u', '--urandom', is_flag=True, default=False, help='random calculate.')
def main(month, day, debug=False, get_all=False, nox=False, urandom=False):
    solver = Solver(month, day, debug, get_all)
    solver.faster_solve(nox, urandom)
