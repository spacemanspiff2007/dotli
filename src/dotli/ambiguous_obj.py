import typing

from .errors import IncompleteListError, SeparatorInKeyError, KeyNotAStringError, KeyAlreadyExistsError


class CMissingEntry:
    def __repr__(self):
        return '<MissingEntry>'


MISSING = CMissingEntry()


class AmbiguousObj:
    def __init__(self, parent_obj: typing.Any, _parent_key: typing.Tuple[str, typing.Optional[int]], stack: tuple):
        self._parent_obj: typing.Optional[AmbiguousObj] = parent_obj
        self._parent_key = _parent_key
        self._stack = stack

        self.dict = {}
        self.list = {}
        self.is_list = True     # keys are only int

    def get_create_child(self, key: str, index: typing.Optional[int], stack: tuple) -> 'AmbiguousObj':
        assert isinstance(key, str)

        child = self.dict.get(key, None)
        if child is not None:
            return child

        child = AmbiguousObj(self, (key, index), stack)
        self.dict[key] = child

        # check list entries while adding them
        if self.is_list:
            if index is None:
                self.is_list = False
            else:
                self.list[index] = child
        return child

    def set(self, key: str, index: typing.Optional[int], value):

        # this can't actually happen so it's just an assertion and not an Exception
        assert key not in self.dict, f'duplicate key: {key}: {self.dict} @ {".".join(self._stack)}'
        self.dict[key] = value

        # check list entries while adding them
        if self.is_list:
            if index is None:
                self.is_list = False
            else:
                self.list[index] = value
        return value

    def reduce(self, fill_list=MISSING) -> typing.Union[list, dict]:
        if self.is_list:
            new_list = []
            for i in range(max(self.list.keys()) + 1):
                try:
                    new_list.append(self.list[i] if fill_list is MISSING else self.list.get(i, fill_list))
                except KeyError:
                    raise IncompleteListError(self._stack, i) from None

            obj = self.list = new_list
        else:
            obj = self.dict

        if self._parent_obj is None:
            return obj

        p = self._parent_obj
        if p.is_list:
            p.list[self._parent_key[1]] = obj

        p.dict[self._parent_key[0]] = obj
        return obj

