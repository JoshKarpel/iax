import datetime
import random

import pytest

from ix import ix


def test_to_jsons():
    @ix
    class JSON:
        a: int
        b: float
        d: str
        e: bool

    jsons = [
        JSON(0, 1.8, 'hi', True),
        JSON(2, 5.3, 'lo', False),
        JSON(-10, -4.2, 'foo', True),
    ]

    expected = '[{"a": 0, "b": 1.8, "d": "hi", "e": true}, {"a": 2, "b": 5.3, "d": "lo", "e": false}, {"a": -10, "b": -4.2, "d": "foo", "e": true}]'

    assert JSON.to_jsons(jsons) == expected


def test_nested_to_jsons():
    @ix
    class Inner:
        a: int

    @ix
    class Outer:
        inner: Inner

    obj = [Outer(Inner(5))]

    expected = '[{"inner": {"a": 5}}]'

    assert Outer.to_jsons(obj) == expected


def test_load_nested_jsons():
    @ix
    class Inner:
        a: int

    @ix
    class Outer:
        inner: Inner

    obj = [Outer(Inner(5))]
    jsons = Outer.to_jsons(obj)

    loaded = list(Outer.from_jsons(jsons))
    assert loaded[0] == obj[0]
