import typing

from .ambiguous_obj import AmbiguousObj, MISSING
from .errors import SeparatorInKeyError, KeyNotAStringError


class Dotli:
    def __init__(self, separator: str = '.', safe: bool = True, list_brackets: bool = False, fill_value_list=MISSING):
        assert isinstance(separator, str), type(separator)

        self.separator: str = separator
        self.safe: bool = safe
        self.list_brackets: bool = list_brackets
        self.fill_value_list = fill_value_list

    def __flt(self, ret: typing.Dict[str, typing.Any], obj: typing.Union[dict, list], key: str, flat_stack: tuple):

        if isinstance(obj, (list, set, tuple)):
            for i, v in enumerate(obj):
                k = str(i) if not self.list_brackets else f'[{i:d}]'
                if self.separator in k:
                    raise SeparatorInKeyError(flat_stack, k, separator=self.separator)

                n_k = key + self.separator + k if key else k
                self.__flt(ret, v, n_k, flat_stack + (f'[{i}]', ))
        elif isinstance(obj, dict):
            for k, v in obj.items():

                if not isinstance(k, str):
                    # un flattening will always result in string keys so we throw this error in safe mode
                    if self.safe:
                        raise KeyNotAStringError(flat_stack, k, value_type=type(k))
                    k = str(k)

                if self.separator in k:
                    raise SeparatorInKeyError(flat_stack, k, separator=self.separator)

                n_k = key + self.separator + k if key else k
                self.__flt(ret, v, n_k, flat_stack + (k, ))
        else:
            # safe mode will ensure that all keys are str so we never overwrite one
            ret[key] = obj

    def flatten(self, _in: typing.Union[list, set, tuple, dict]) -> typing.Dict[str, typing.Any]:
        ret = {}
        self.__flt(ret, _in, '', ('root', ))
        return ret

    def __uflt(self, obj: AmbiguousObj, keys, val, key_stack: tuple, objs: typing.Set[AmbiguousObj]):
        l_k = len(keys)
        key: str = keys[0]
        key_stack = key_stack + (key, )

        # index of the list has to be int or None
        index: typing.Union[None, str, int] = None
        if obj.is_list:
            if self.list_brackets:
                if key[0] == '[' and key[-1] == ']':
                    index = key[1:-1]
                    index = int(index) if index.isdecimal() else None
            else:
                index = int(key) if key.isdecimal() else None

        if l_k == 1:
            obj.set(key, index, val)
            return

        new_obj = obj.get_create_child(key, index, key_stack)
        objs.add(new_obj)
        self.__uflt(new_obj, keys[1:], val, key_stack, objs)

    def unflatten(self, _in: typing.Dict[str, typing.Any]) -> typing.Union[typing.Iterable, typing.Mapping]:

        _in = {tuple(k.split(self.separator)): v for k, v in _in.items()}

        # check if the root element may be a list
        ret = AmbiguousObj(None, (None, None), ('root', ))
        objs = set()

        for keys, val in _in.items():
            self.__uflt(ret, keys, val, tuple(), objs)

        for obj in objs:
            obj.reduce(self.fill_value_list)

        return ret.reduce(self.fill_value_list)
