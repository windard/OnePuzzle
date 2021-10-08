# -*- coding: utf-8 -*-

from one_puzzle.element import Block, JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC


def test_jan():
    assert JAN.row == 1
    assert JAN.col == 1

    assert JAN().row == 1
    assert JAN().col == 1


def test_feb():
    assert FEB.row == 1
    assert FEB.col == 2

    assert FEB().row == 1
    assert FEB().col == 2


def test_mar():
    assert MAR.row == 1
    assert MAR.col == 3

    assert MAR().row == 1
    assert MAR().col == 3


def test_apr():
    assert APR.row == 1
    assert APR.col == 4

    assert APR().row == 1
    assert APR().col == 4


def test_may():
    assert MAY.row == 1
    assert MAY.col == 5

    assert MAY().row == 1
    assert MAY().col == 5


def test_jun():
    assert JUN.row == 1
    assert JUN.col == 6

    assert JUN().row == 1
    assert JUN().col == 6


def test_jul():
    assert JUL.row == 2
    assert JUL.col == 1

    assert JUL().row == 2
    assert JUL().col == 1


def test_aug():
    assert AUG.row == 2
    assert AUG.col == 2

    assert AUG().row == 2
    assert AUG().col == 2


def test_sep():
    assert SEP.row == 2
    assert SEP.col == 3

    assert SEP().row == 2
    assert SEP().col == 3


def test_oct():
    assert OCT.row == 2
    assert OCT.col == 4

    assert OCT().row == 2
    assert OCT().col == 4


def test_nov():
    assert NOV.row == 2
    assert NOV.col == 5

    assert NOV().row == 2
    assert NOV().col == 5


def test_dec():
    assert DEC.row == 2
    assert DEC.col == 6

    assert DEC().row == 2
    assert DEC().col == 6


def test_block():
    assert Block(1, 1).col == 1
    assert Block(1, 1).row == 1

    assert Block(1, 1) == Block(1, 1)
    assert repr(Block(1, 1)) == "Block(1, 1)"
