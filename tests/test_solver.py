# -*- coding: utf-8 -*-

from one_puzzle.element import Block
from one_puzzle.solver import Solver


class TestSolver(object):
    def test_get_around(self):
        block = Block(2, 3)
        surrounds = Solver.get_around(block)
        assert len(surrounds) == 4
        assert surrounds == {Block(2, 4), Block(3, 3), Block(1, 3), Block(2, 2)}

    def test_validate_trap(self):
        blocks = [Block(2, 3), Block(2, 4), Block(3, 3), Block(1, 3), Block(2, 2)]
        solver = Solver()

        assert solver.validate_trap([])
        assert solver.validate_trap(blocks)
        assert not solver.validate_trap([Block(2, 3), Block(2, 4)])
