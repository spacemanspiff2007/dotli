import dotli
from dotli import Dotli
import pytest


def test_flatten_exception_sep_in_key():
    # list keys
    with pytest.raises(dotli.errors.SeparatorInKeyError) as e:
        Dotli(separator='1').flatten({'a': [0, 1]})
    assert str(e.value) == 'Separator "1" is in key "1"! @ root.a'

    with pytest.raises(dotli.errors.SeparatorInKeyError) as e:
        Dotli(separator='1').flatten([[[0, 1]]])
    assert str(e.value) == 'Separator "1" is in key "1"! @ root.[0].[0]'

    # dict keys
    with pytest.raises(dotli.errors.SeparatorInKeyError) as e:
        Dotli(separator='.').flatten({'a.a': {'a': 'b'}})
    assert str(e.value) == 'Separator "." is in key "a.a"! @ root'

    with pytest.raises(dotli.errors.SeparatorInKeyError) as e:
        Dotli(separator='.').flatten({'a': {'b': {'c.c': 'd'}}})
    assert str(e.value) == 'Separator "." is in key "c.c"! @ root.a.b'


def test_flatten_exception_key_not_str():
    with pytest.raises(dotli.errors.KeyNotAStringError) as e:
        Dotli().flatten({'a': {1: 1}})
    assert str(e.value) == 'Key "1" (<class \'int\'>) is not a string! @ root.a'

    # this check can be disabled with the safe flag
    assert Dotli(safe=False).flatten({'a': {1: 1}}) == {'a.1': 1}


def test_incomplete_list():
    with pytest.raises(dotli.errors.IncompleteListError) as e:
        Dotli().unflatten({'a.0': 1, 'a.2': 2})

    assert str(e.value) == 'No entry for index "1" in list! @ a'
