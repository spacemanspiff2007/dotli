# Dotli
---
![Test Status](https://github.com/spacemanspiff2007/dotli/workflows/Tests/badge.svg)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dotli)](https://github.com/spacemanspiff2007/dotli)
[![PyPI](https://img.shields.io/pypi/v/dotli)](https://github.com/spacemanspiff2007/dotli)
[![Downloads](https://pepy.tech/badge/dotli/month)](https://pepy.tech/project/dotli/month)

Yet another library for flattening structures

## Installation
```bash
pip install dotli
```

## Usage

### flatten

```python
from dotli import Dotli

data = {
    'a': {
        'c': 'val1',
        'd': 'val2',
    },
    'b': {
        'c': 2,
        'd': {'key3': 'val3', 'key4': 'val4'},
    }
}

d = Dotli()                 # create an obj with a default configuration
flat = d.flatten(data)      # flatten
orig = d.unflatten(flat)    # unflatten
assert data == orig
print(flat)
```

```python
{
  'a.c': 'val1',
  'a.d': 'val2',
  'b.c': 2,
  'b.d.key3': 'val3',
  'b.d.key4': 'val4',
}
```

The separator can be configured
```python
data = {
    'a': {'c': 'd'},
    'b': {'e': 'f'}
}

d = Dotli(separator='-')
print(d.flatten(data))
```

```python
{
  'a-c': 'd',
  'b-e': 'f',
}
```

It is also possible to flatten lists and a mixture of lists and dicts

```python
data = {
    'a': {
        'c': [1, 2, 3],
        'd': ['e1', 'e2', 'e3'],
    },
    'b': 'h'
}

d = Dotli()
print(d.flatten(data))
```

```python
{
  'a.c.0': 1,
  'a.c.1': 2,
  'a.c.2': 3,
  'a.d.0': 'e1',
  'a.d.1': 'e2',
  'a.d.2': 'e3',
  'b': 'h',
}
```

List indices can be wrapped in square brackets to allow numerical strings in dicts as keys

```python
data = {
    'a': {
        '1': [1, 2, 3],
        '2': ['e1', 'e2', 'e3'],
    },
    'b': 'h'
}

d = Dotli(list_brackets=True)
flat = d.flatten(data)
orig = d.unflatten(flat)
assert data == orig
print(flat)
```

```python
{
  'a.1.[0]': 1,
  'a.1.[1]': 2,
  'a.1.[2]': 3,
  'a.2.[0]': 'e1',
  'a.2.[1]': 'e2',
  'a.2.[2]': 'e3',
  'b': 'h',
}
```


There will be a nice error message if the dict can not be flattened including the path to the invalid element.

```python
from dotli.errors import SeparatorInKeyError

data = {
    'a': {
        'b.b': 1,
    },
    'b': 'h'
}
try:
    Dotli().flatten(data)
except SeparatorInKeyError as e:
    print(e)
```

```
Separator "." is in key "b.b"! @ root.a
```

### unflatten

When elements are missing in a list Dotli will throw an error

```python
from dotli.errors import IncompleteListError

data = {
    'a.0': 0,
    'a.2': 2,
}
try:
    d = Dotli()
    d.unflatten(data)
except IncompleteListError as e:
    print(e)
```

```
No entry for index "1" in list! @ a
```

However it is possible to specify a fill value 
which will automatically be inserted into the list for missing entries

```python
data = {
    'a.0': 0,
    'a.2': 2,
}

d = Dotli(fill_value_list=None)
print(d.unflatten(data))
```

```python
{
  'a': [0, None, 2],
}
```