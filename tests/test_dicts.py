from dotli import Dotli


def test_short():
    data = {'a': 1, 'b': 2}
    result = {'a': 1, 'b': 2,}

    d = Dotli()
    assert d.flatten(data) == result
    assert data == d.unflatten(result)


def test_nested():
    data = {'a': {'d': 'e'}, 'b': {'f': 'g', 'h': 'i'}}
    result = {'a.d': 'e', 'b.f': 'g', 'b.h': 'i'}

    d = Dotli()
    assert d.flatten(data) == result
    assert data == d.unflatten(result)


def test_deep_nested():
    data = {'a': {'b': {'0': 1, 'c': 2}, 'd': 'e'}}
    result = {'a.b.0': 1, 'a.b.c': 2, 'a.d': 'e'}

    d = Dotli()
    assert d.flatten(data) == result
    assert data == d.unflatten(result)

    d = Dotli(separator='-')
    result = {'a-b-0': 1, 'a-b-c': 2, 'a-d': 'e'}
    assert d.flatten(data) == result
    assert data == d.unflatten(result)


def test_digit_in_dict():
    data = {
        'a': {'0': {'c': 2}, 'a': {'c': 4}},
    }
    result = {'a.0.c': 2, 'a.a.c': 4}

    d = Dotli(list_brackets=False)
    assert d.flatten(data) == result
    assert data == d.unflatten(result)

    data = {
        'a': {'0': 0, 'a': 1},
    }
    result = {'a.0': 0, 'a.a': 1}

    d = Dotli(list_brackets=False)
    assert d.flatten(data) == result
    assert data == d.unflatten(result)


def test_int_keys_dict():
    data = {'a': {'1': [1], '2': ['e1'],}}
    result = {'a.1.[0]': 1, 'a.2.[0]': 'e1'}

    d = Dotli(list_brackets=True)
    assert d.flatten(data) == result
    assert data == d.unflatten(result)
