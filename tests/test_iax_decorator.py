import pytest

from iax import iax


def test_iax_with_no_kwargs():
    @iax
    class Foo:
        a: int

    assert Foo.__iax__
    assert '__eq__' in Foo.__dict__


def test_iax_with_kwargs():
    @iax(eq = False)
    class Foo:
        a: int

    assert Foo.__iax__
    assert '__eq__' not in Foo.__dict__
