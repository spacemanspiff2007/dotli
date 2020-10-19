from dotli import Dotli


def test_short():
    data = ['1', '2', '3']
    result = {'0': '1', '1': '2', '2': '3', }

    d = Dotli()
    assert d.flatten(data) == result
    assert data == d.unflatten(result)

    d = Dotli(list_brackets=True)
    result = {'[0]': '1', '[1]': '2', '[2]': '3', }
    assert d.flatten(data) == result
    assert data == d.unflatten(result)


def test_nested():
    data = [['a', 'b', 'c'], ['d', 'e', 'f']]
    result = {'0.0': 'a', '0.1': 'b', '0.2': 'c', '1.0': 'd', '1.1': 'e', '1.2': 'f'}

    d = Dotli()
    assert d.flatten(data) == result
    assert data == d.unflatten(result)

    d = Dotli(list_brackets=True)
    result = {'[0].[0]': 'a', '[0].[1]': 'b', '[0].[2]': 'c', '[1].[0]': 'd', '[1].[1]': 'e', '[1].[2]': 'f'}
    assert d.flatten(data) == result
    assert data == d.unflatten(result)

    d = Dotli(list_brackets=True, separator='-')
    result = {'[0]-[0]': 'a', '[0]-[1]': 'b', '[0]-[2]': 'c', '[1]-[0]': 'd', '[1]-[1]': 'e', '[1]-[2]': 'f'}
    assert d.flatten(data) == result
    assert data == d.unflatten(result)


def test_fill_value():
    d = Dotli(fill_value_list=None)
    assert d.unflatten({'0': 0, '2': 0}) == [0, None, 0]
