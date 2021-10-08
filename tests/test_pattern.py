# -*- coding: utf-8 -*-

from one_puzzle.element import Block
from one_puzzle.pattern import BigLEntity, BigZEntity, FullSmashEntity


def test_big_l():
    entity = BigLEntity()

    assert entity.blocks == [Block(1, 1), Block(2, 1), Block(3, 1), Block(4, 1), Block(4, 2)]
    assert entity.rotate().blocks == [Block(1, 0), Block(1, 2), Block(1, 3), Block(1, 4), Block(2, 4)]
    assert entity.horizontal().blocks == [Block(1, 4), Block(1, 3), Block(1, 2), Block(1, 1), Block(2, 1)]
    assert entity.vertical().blocks == [Block(2, 4), Block(2, 3), Block(2, 2), Block(2, 1), Block(1, 1)]


def test_big_z():
    entity = BigZEntity()

    assert entity.blocks == [Block(1, 1), Block(1, 2), Block(2, 2), Block(3, 2), Block(3, 3)]
    assert entity.rotate().blocks == [Block(1, 1), Block(2, 1), Block(2, 2), Block(2, 3), Block(3, 3)]
    assert entity.horizontal().blocks == [Block(1, 3), Block(2, 3), Block(2, 2), Block(2, 1), Block(3, 1)]
    assert entity.vertical().blocks == [Block(3, 3), Block(2, 3), Block(2, 2), Block(2, 1), Block(1, 1)]


def test_full_smash():
    entity = FullSmashEntity()

    assert entity.blocks == [Block(1, 1), Block(2, 1), Block(1, 2), Block(2, 2), Block(1, 3), Block(2, 3)]
    assert entity.rotate().blocks == [Block(1, 1), Block(1, 2), Block(2, 1), Block(2, 2), Block(3, 1), Block(3, 2)]
    assert entity.horizontal().blocks == [Block(1, 2), Block(1, 1), Block(2, 2), Block(2, 1), Block(3, 2), Block(3, 1)]
    assert entity.vertical().blocks == [Block(3, 2), Block(3, 1), Block(2, 2), Block(2, 1), Block(1, 2), Block(1, 1)]
