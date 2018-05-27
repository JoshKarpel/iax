import pytest

import random

from ix import ix


def test_ints_to_csvs_with_header():
    @ix
    class Ints:
        a: int
        b: int

    ints = [
        Ints(0, 1),
        Ints(2, 5),
        Ints(-10, -4),
    ]

    expected = "a,b\n0,1\n2,5\n-10,-4"

    assert Ints.to_csvs(ints, write_header = True) == expected


def test_ints_to_csvs_no_header():
    @ix
    class Ints:
        a: int
        b: int

    ints = [
        Ints(0, 1),
        Ints(2, 5),
        Ints(-10, -4),
    ]

    expected = "0,1\n2,5\n-10,-4"
    assert Ints.to_csvs(ints) == expected
