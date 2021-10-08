# -*- coding: utf-8 -*-

from one_puzzle.element import Block, JAN, DEC


def test_jan():
    assert JAN.col == 1
    assert JAN.row == 1

    assert JAN().col == 1
    assert JAN().row == 1


def test_dec():
    assert DEC.row == 2
    assert DEC.col == 6

    assert DEC().row == 2
    assert DEC().col == 6


def test_block():
    assert Block(1, 1).col == 1
    assert Block(1, 1).row == 1

    assert Block(1, 1) == Block(1, 1)
    assert repr(Block(1, 1)) == "<Block/1-1>"
