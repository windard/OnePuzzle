# -*- coding: utf-8 -*-
import click
import random
import datetime

from queue import Queue

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

    def solve(self, nox=False):
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

        def traceback(classes, entities, entity_filled):
            if not classes:
                return

            entity_class = classes.pop()
            for i in range(7):
                for j in range(7):

                    for m in [lambda x: x, lambda x: x.rotate()]:
                        for n in [lambda x: x, lambda x: x.horizontal()]:
                            for p in [lambda x: x, lambda x: x.vertical()]:

                                self.calculated += 1
                                entity = entity_class(i, j)
                                entity = m(n(p(entity)))

                                entities.append(entity)

                                entity_filled.extend(entity.blocks)
                                entity_filled_set = set(entity_filled)

                                # 有超出的
                                if entity_filled_set - totals:
                                    entities.remove(entity)
                                    for block in entity.blocks:
                                        entity_filled.remove(block)
                                    continue

                                # 有重复的
                                if len(entity_filled) != len(entity_filled_set):
                                    entities.remove(entity)
                                    for block in entity.blocks:
                                        entity_filled.remove(block)
                                    continue

                                left_blocks = totals - entity_filled_set
                                # 有成功
                                if not left_blocks:
                                    if self.debug:
                                        print("success in {}:{}".format(self.calculated, entities))

                                    result.append(entities)
                                    if not self.get_all:
                                        return entities

                                # 有空洞
                                if not self.validate_trap(left_blocks):
                                    entities.remove(entity)
                                    for block in entity.blocks:
                                        entity_filled.remove(block)
                                    continue

                                # 成功则无需再清空
                                success_result = traceback(classes, entities, entity_filled)
                                if success_result:
                                    return success_result

                                # 清空再继续努力
                                entities.remove(entity)
                                for block in entity.blocks:
                                    entity_filled.remove(block)

            classes.append(entity_class)

        random.shuffle(self.entity_classes)

        if self.debug:
            print("start at:{}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        success_entities = traceback(self.entity_classes, [], [])

        if self.debug:
            print("end   at:{}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            print("calculated times:{}".format(self.calculated))
            print("success entities:{}".format(success_entities))

        if self.get_all:
            print("groups number:{}".format(len(result)))
            print("all success group:{}".format(result))

        for success in success_entities:
            board.add_entity(success)
        board.show()


@click.command()
@click.help_option("-h", "--help")
@click.argument('month', type=int)
@click.argument('day', type=int)
@click.option('-d', '--debug', is_flag=True, default=False, help='show debug message.')
@click.option('-a', '--all', 'get_all', is_flag=True, default=False, help='get all result.')
@click.option('-n', '--nox', is_flag=True, default=False, help='no screen show.')
def main(month, day, debug=False, get_all=False, nox=False):
    solver = Solver(month, day, debug, get_all)
    solver.solve(nox)
