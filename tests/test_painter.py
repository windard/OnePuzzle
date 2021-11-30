# -*- coding: utf-8 -*-
from one_puzzle.element import Block
from one_puzzle.painter import CliPainter, Painter, QtPainter, RichPainter
from one_puzzle.pattern import (
    SunkenEntity,
    ConvexEntity,
    StilettoEntity,
    EquilateralLEntity,
    FullSmashEntity,
    LackSmashEntity,
    BigZEntity,
    BigLEntity,
)


def test_cli_painter():
    assert issubclass(CliPainter, Painter)
    assert issubclass(QtPainter, Painter)
    assert issubclass(RichPainter, Painter)


def test_painter_show(capsys):
    success_entities = {
        SunkenEntity: {Block(3, 3), Block(4, 2), Block(4, 3), Block(2, 2), Block(2, 3)},
        ConvexEntity: {Block(3, 2), Block(4, 1), Block(1, 1), Block(2, 1), Block(3, 1)},
        StilettoEntity: {Block(7, 3), Block(4, 4), Block(5, 3), Block(5, 4), Block(6, 3)},
        EquilateralLEntity: {Block(3, 4), Block(1, 2), Block(1, 3), Block(1, 4), Block(2, 4)},
        FullSmashEntity: {Block(6, 6), Block(6, 7), Block(4, 6), Block(4, 7), Block(5, 6), Block(5, 7)},
        LackSmashEntity: {Block(7, 1), Block(5, 1), Block(5, 2), Block(6, 1), Block(6, 2)},
        BigZEntity: {Block(3, 6), Block(3, 7), Block(1, 5), Block(1, 6), Block(2, 6)},
        BigLEntity: {Block(6, 4), Block(6, 5), Block(3, 5), Block(4, 5), Block(5, 5)},
    }

    for entity_class, blocks in success_entities.items():
        for block in blocks:
            block.entity = entity_class

    CliPainter().show(success_entities)
    captured = capsys.readouterr()
    assert (
        captured.out
        == """ &  *  *  *  $  $    
 &  %  %  *     $    
 &  &  %  *  +  $  $ 
 &  %  %  ^  +  @  @ 
 #  #  ^  ^  +  @  @ 
 #  #  ^  +  +  @  @ 
 #     ^             
"""
    )
