from dotli import Dotli


def test_flatten_list_start():
    data = [
        {'b': 1, 'c': 2, },
        {'e': 3, 'f': 4, },
    ]

    result = {
        '0.b': 1,
        '0.c': 2,
        '1.e': 3,
        '1.f': 4,
    }

    d = Dotli()
    assert d.flatten(data) == result
    assert data == d.unflatten(result)


def test_flatten_list_mid():
    data = {
        'a': [
            {'b': 1, 'c': 2, },
            {'e': 3, 'f': 4, },
        ]
    }

    result = {
        'a.0.b': 1,
        'a.0.c': 2,
        'a.1.e': 3,
        'a.1.f': 4,
    }

    d = Dotli()
    assert d.flatten(data) == result
    assert data == d.unflatten(result)


def test_flatten_list_end():
    data = {
        'a': {'b': [1, 2, 3], 'c': [4, 5, 6], },
        'd': [7, 8, 9],
    }

    result = {
        'a.b.0': 1,
        'a.b.1': 2,
        'a.b.2': 3,
        'a.c.0': 4,
        'a.c.1': 5,
        'a.c.2': 6,
        'd.0': 7,
        'd.1': 8,
        'd.2': 9,
    }

    d = Dotli()
    assert d.flatten(data) == result
    assert data == d.unflatten(result)

    result = {
        'a.b.[0]': 1,
        'a.b.[1]': 2,
        'a.b.[2]': 3,
        'a.c.[0]': 4,
        'a.c.[1]': 5,
        'a.c.[2]': 6,
        'd.[0]': 7,
        'd.[1]': 8,
        'd.[2]': 9,
    }

    d = Dotli(list_brackets=True)
    assert d.flatten(data) == result
    assert data == d.unflatten(result)
